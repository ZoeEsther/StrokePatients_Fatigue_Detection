import time


class AttentionScorer:

    def __init__(self, fps=20, ear_threshold=0.25,  ear_time_threshold=3.0, perclos_threshold=0.2,
                 pitch_threshold=45, yaw_threshold=30, roll_threshold=170,pose_time_threshold=3.0,
                 mouth_threshold=0.7,mouth_time_threshold=2,verbose=False):
        self.fps = fps

        self.perclos_time_period = 60
        self.perclos_threshold = perclos_threshold

        # the time threshold are divided for the estimated frame time
        # (that is a function passed parameter and so can vary)
        self.ear_threshold = ear_threshold
        self.ear_time_threshold = ear_time_threshold
        self.ear_counter = 0
        self.eye_closure_counter = 0

        self.mouth_threshold = mouth_threshold
        self.mouth_time_threshold = mouth_time_threshold
        self.mouth_counter = 0
        self.mouth_open_counter = 0

        self.roll_threshold = roll_threshold
        self.pitch_threshold = pitch_threshold
        self.yaw_threshold = yaw_threshold
        self.pose_time_threshold = pose_time_threshold
        self.pose_counter = 0

        self.verbose = verbose

    # def get_PERCLOS(self, ear_score, mouth_score):
    #
    #     tired = False
    #
    #     if (ear_score is not None) and (ear_score <= self.ear_threshold):
    #         if not tired:
    #             self.eye_closure_counter += 1
    #     elif self.eye_closure_counter > 0:
    #         self.eye_closure_counter -= 1
    #
    #     if (mouth_score is not None) and (mouth_score >= self.mouth_threshold):
    #         if not tired:
    #             self.mouth_open_counter += 1
    #     elif self.mouth_open_counter > 0:
    #         self.mouth_open_counter -= 1
    #
    #     eye_closure_time = (self.eye_closure_counter / self.fps)
    #     perclos_score = eye_closure_time / self.perclos_time_period
    #
    #     mouth_open_time = (self.mouth_open_counter / self.fps)
    #
    #     if (perclos_score >= self.perclos_threshold) or (mouth_open_time >= self.mouth_time_threshold):  # if the PERCLOS score is higher than a threshold, tired = True
    #         tired = True
    #         self.eye_closure_counter = 0
    #
    #     if self.verbose:
    #         print(f"eye closed:{tired}")
    #
    #     return tired, eye_closure_time, mouth_open_time

    def eval_scores(self, ear_score,mouth_score, head_pitch, head_yaw,head_roll):

        asleep = False
        distracted = False
        tired = False
        # 昏睡判断：眼睛闭合超过3s
        if (ear_score is not None) and (ear_score <= self.ear_threshold):
            if not asleep:
                self.ear_counter += 1
        elif self.ear_counter > 0:
            self.ear_counter -= 1
        if (self.ear_counter/self.fps) >= self.ear_time_threshold:  # check if the ear cumulative counter surpassed the threshold
            asleep = True
        # 疲劳判断：打哈欠 或 PERCLOS
        if (ear_score is not None) and (ear_score <= self.ear_threshold):
            if not tired:
                self.eye_closure_counter += 1
        elif self.eye_closure_counter > 0:
            self.eye_closure_counter -= 1
        if (mouth_score is not None) and (mouth_score >= self.mouth_threshold):
            if not tired:
                self.mouth_open_counter += 1
        elif self.mouth_open_counter > 0:
            self.mouth_open_counter -= 1
        eye_closure_time = (self.eye_closure_counter / self.fps)
        perclos_score = eye_closure_time / self.perclos_time_period
        mouth_open_time = (self.mouth_open_counter / self.fps)
        if (perclos_score >= self.perclos_threshold) or (mouth_open_time >= self.mouth_time_threshold):
            # if the PERCLOS score is higher than a threshold, tired = True
            tired = True
            self.eye_closure_counter = 0
        # 分神判断： 头部三个角度范围
        if (   ((head_pitch is not None) and (abs(head_pitch) > self.pitch_threshold))
            or ((head_yaw is not None) and (abs(head_yaw) > self.yaw_threshold))
            or ((head_roll is not None) and (abs(head_roll) > self.roll_threshold)) ):

            if not distracted:
                self.pose_counter += 1
        elif self.pose_counter > 0:
            self.pose_counter -= 1

        if (self.pose_counter/self.fps) >= self.pose_time_threshold:  # check if the pose cumulative counter surpassed the threshold
            distracted = True


        if self.verbose:  # print additional info if verbose is True
           print(
                f"Asleep!:{asleep}\t Distracted!:{distracted}")

        return asleep,tired, distracted
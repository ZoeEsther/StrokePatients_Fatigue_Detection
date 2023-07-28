import cv2
import numpy as np
import Utils
# from .Utils import rotationMatrixToEulerAngles, draw_pose_info


class HeadPoseEstimator:

    def __init__(self, camera_matrix=None, dist_coeffs=None, show_axis: bool = False):
        """
        Head Pose estimator class that contains the get_pose method for computing the three euler angles
        (roll, pitch, yaw) of the head. It uses the image/frame, the dlib detected landmarks of the head and,
        optionally the camera parameters

        Parameters
        ----------
        camera_matrix: numpy array
            Camera matrix of the camera used to capture the image/frame
        dist_coeffs: numpy array
            Distortion coefficients of the camera used to capture the image/frame
        show_axis: bool
            If set to True, shows the head pose axis projected from the nose keypoint and the face landmarks points
            used for pose estimation (default is False)
        """

        self.verbose = show_axis
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs

    def get_pose(self, frame, landmarks):
        """
        Estimate head pose using the head pose estimator object instantiated attribute

        Parameters
        ----------
        frame: numpy array
            Image/frame captured by the camera
        landmarks: dlib.rectangle
            Dlib detected 68 landmarks of the head

        Returns
        --------
        - if successful: image_frame, roll, pitch, yaw (tuple)
        - if unsuccessful: None,None,None,None (tuple)

        """
        self.keypoints = landmarks  # dlib 68 landmarks
        self.frame = frame  # opencv image array

        self.axis = np.float32([[3, 0, 0],
                                [0, 3, 0],
                                [0, 0, 3]]).reshape(-1,3)
        # array that specify the length of the 3 projected axis from the nose

        if self.camera_matrix is None:
            # if no camera matrix is given, estimate camera parameters using picture size
            self.size = frame.shape
            self.focal_length = self.size[1]
            self.center = (self.size[1] / 2, self.size[0] / 2)

            self.camera_matrix = np.array(
                [[self.focal_length, 0, self.center[0]],
                 [0, self.focal_length, self.center[1]],
                 [0, 0, 1]], dtype="double"
            )


        if self.dist_coeffs is None:  # if no distorsion coefficients are given, assume no lens distortion
            self.dist_coeffs = np.zeros((4, 1))

        # 3D Head model world space points (generic human head)
        self.model_points = np.array([
            # (0.0, 0.0, 0.0),  # Nose tip
            # (0.0, -330.0, -65.0),  # Chin
            # (-225.0, 170.0, -135.0),  # Left eye left corner
            # (225.0, 170.0, -135.0),  # Right eye right corner
            # (-150.0, -150.0, -125.0),  # Left Mouth corner
            # (150.0, -150.0, -125.0)  # Right mouth corner
            (6.825897, 6.760612, 4.402142),  # 左眉左角，3D：33；2D：17
            (1.330353, 7.122144, 6.903745),  # 左眉右角，3D：29；2D：21

            (-1.330353, 7.122144, 6.903745),  # 右眉左角，3D：34；2D：22
            (-6.825897, 6.760612, 4.402142),  # 右眉右角，3D：38；2D：26

            (5.311432, 5.485328, 3.987654),  # 左眼左角，3D：13；2D：36
            (1.789930, 5.393625, 4.413414),  # 左眼右角，3D：17；2D：39

            (-1.789930, 5.393625, 4.413414),  # 右眼左角，3D：25；2D：42
            (-5.311432, 5.485328, 3.987654),  # 右眼右角，3D：21；2D：45

            (2.005628, 1.409845, 6.165652),  # 鼻子左角，3D：55；2D：31
            (-2.005628, 1.409845, 6.165652),  # 鼻子右角，3D：49；2D：35

            (2.774015, -2.080775, 5.048531),  # 嘴巴左角，3D：43；2D：48
            (-2.774015, -2.080775, 5.048531),  # 嘴巴右角，3D：39；2D：54
            (0.000000, -3.116408, 6.097667),  # 嘴巴中下角，3D：45；2D：57

            (0.000000, -7.415691, 4.070434),  # 下巴底部，3D：6；2D：8

        ], dtype="double")

        # 2D Point position of dlib face keypoints used for pose estimation
        self.image_points = np.array([
            # (landmarks.part(30).x, landmarks.part(30).y),  # Nose tip
            # (landmarks.part(8).x, landmarks.part(8).y),  # Chin
            # (landmarks.part(36).x, landmarks.part(36).y),  # Left eye left corner
            # (landmarks.part(45).x, landmarks.part(45).y),  # Right eye right corne
            # (landmarks.part(48).x, landmarks.part(48).y),  # Left Mouth corner
            # (landmarks.part(54).x, landmarks.part(54).y)  # Right mouth corner
            (landmarks.part(17).x, landmarks.part(17).y),  # 左眉左角
            (landmarks.part(21).x, landmarks.part(21).y),  # 左眉右角

            (landmarks.part(22).x, landmarks.part(22).y),  # 右眉左角
            (landmarks.part(26).x, landmarks.part(26).y),  # 右眉右角

            (landmarks.part(36).x, landmarks.part(36).y),  # 左眼左角
            (landmarks.part(39).x, landmarks.part(39).y),  # 左眼右角

            (landmarks.part(42).x, landmarks.part(42).y),  # 右眼左角
            (landmarks.part(45).x, landmarks.part(45).y),  # 右眼右角

            (landmarks.part(31).x, landmarks.part(31).y),  # 鼻子左角
            (landmarks.part(35).x, landmarks.part(35).y),  # 鼻子右角

            (landmarks.part(48).x, landmarks.part(48).y),  # 嘴巴左角
            (landmarks.part(54).x, landmarks.part(54).y),  # 嘴巴右角
            (landmarks.part(57).x, landmarks.part(57).y),  # 嘴巴中下角

            (landmarks.part(8).x, landmarks.part(8).y),  # 下巴底角
        ], dtype="double")

        _,rvec, tvec = cv2.solvePnP(self.model_points, self.image_points,self.camera_matrix, self.dist_coeffs,
                                    flags=cv2.SOLVEPNP_ITERATIVE)
        nose = (int(landmarks.part(30).x), int(landmarks.part(30).y))
        (nose_end_point2D, _) = cv2.projectPoints(self.axis, rvec, tvec, self.camera_matrix, self.dist_coeffs)

        rvec_matrix = cv2.Rodrigues(rvec)[0]
        proj_matrix = np.hstack((rvec_matrix, tvec))
        eulerAngles = -cv2.decomposeProjectionMatrix(proj_matrix)[6]
        pitch = eulerAngles[0][0]
        yaw = eulerAngles[1][0]
        roll = eulerAngles[2][0]


        if self.verbose:
            self.frame = Utils.draw_pose_info(
                self.frame, nose, nose_end_point2D, roll, pitch, yaw)
            # draws 3d axis from the nose and to the computed projection points
            for point in self.image_points:
                cv2.circle(self.frame, tuple(
                    point.ravel().astype(int)), 2, (0, 255, 255), -1)
            # draws the 14 keypoints used for the pose estimation

        return self.frame, roll, pitch, yaw

        # # compute the pose of the head using the image points and the 3D model points
        # (success, rvec, tvec) = cv2.solvePnP(self.model_points, self.image_points,
        #                                      self.camera_matrix, self.dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

        # if success:  # if the solvePnP succeed, compute the head pose, otherwise return None
        #
        #     rvec, tvec = cv2.solvePnPRefineVVS(
        #         self.model_points, self.image_points, self.camera_matrix, self.dist_coeffs, rvec, tvec)
        #     # this method is used to refine the rvec and tvec prediction
        #
        #     # Head nose point in the image plane
        #     nose = (int(landmarks.part(30).x), int(landmarks.part(30).y))
        #
        #     # this function computes the 3 projection axis from the nose point of the head, so we can use them to
        #     # show the head pose later
        #     (nose_end_point2D, _) = cv2.projectPoints(
        #         self.axis, rvec, tvec, self.camera_matrix, self.dist_coeffs)
        #
        #     # using the Rodrigues formula, this functions computes the Rotation Matrix from the rotation vector
        #     Rmat = cv2.Rodrigues(rvec)[0]
        #
        #     roll, pitch, yaw = rotationMatrixToEulerAngles(Rmat) * 180/np.pi
        #
        #     """
        #     We use the rotationMatrixToEulerAngles function to compute the euler angles (roll, pitch, yaw) from the
        #     Rotation Matrix. This function also checks if we have a gymbal lock.
        #     The angles are converted from radians to degrees
        #
        #     An alternative method to compute the euler angles is the following:
        #
        #     P = np.hstack((Rmat,tvec)) -> computing the projection matrix
        #     euler_angles = -cv2.decomposeProjectionMatrix(P)[6] -> extracting euler angles for yaw pitch and roll from the projection matrix
        #     """
        #
        #     if self.verbose:
        #         self.frame = draw_pose_info(
        #             self.frame, nose, nose_end_point2D, roll, pitch, yaw)
        #         # draws 3d axis from the nose and to the computed projection points
        #         for point in self.image_points:
        #             cv2.circle(self.frame, tuple(
        #                 point.ravel().astype(int)), 2, (0, 255, 255), -1)
        #         # draws the 6 keypoints used for the pose estimation
        #
        #     return self.frame, roll, pitch, yaw
        #
        # else:
        #     return None, None, None, None

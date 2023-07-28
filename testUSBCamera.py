from PyCameraList.camera_device import test_list_cameras, list_video_devices, list_audio_devices
import cv2



cameras = list_video_devices()
print(f'======================  camera_list:{cameras}')
idx = 0
camera_id = cameras[idx][0]
camera_name = cameras[idx][1]
print(f'\n======================  preview camera:camera_id={camera_id} camera_name={camera_name}')
cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
cap.set(cv2.CAP_PROP_FPS, 30)
i = 0
while True:
    suc, frame = cap.read()
    if not suc:
        break
    cv2.imshow("preview camera", frame)
    cv2.waitKey(30)
    i += 1

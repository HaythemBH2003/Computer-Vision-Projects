import cv2
import mediapipe
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()
min_volume, max_volume = volume_range[0], volume_range[1]
detected_volume = 0
display_volume = 400
percentage = 0

camera_width, camera_height = 640, 480
previous_time = 0

cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)

detector = htm.hand_detector(detection_confidence=0.7)

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)
    
    if len(lmList) > 0:
        print(lmList[4], lmList[8])
        
        x1, y1 = int(lmList[4][1]), int(lmList[4][2])
        x2, y2 = int(lmList[8][1]), int(lmList[8][2])
        middle_x, middle_y = int((x1 + x2) / 2), int((y1 + y2) / 2)

        cv2.circle(img, (x1, y1), 10, (238, 172, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (238, 172, 0), cv2.FILLED)
        cv2.circle(img, (middle_x, middle_y), 10, (255, 255, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        min_length = 20
        max_length = 120

        detected_volume = np.interp(length, [min_length, max_length], [min_volume, max_volume])
        display_volume = np.interp(length, [min_length, max_length], [400, 150])
        percentage = np.interp(length, [min_length, max_length], [0, 100])
        volume.SetMasterVolumeLevel(detected_volume, None)
        print(detected_volume)

        if length < 50:
            cv2.circle(img, (middle_x, middle_y), 10, (255, 70, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (238, 172, 0), 3)
        cv2.rectangle(img, (50, int(display_volume)), (85, 400), (238, 172, 0), cv2.FILLED)
        cv2.putText(img, f"{int(percentage)} %", (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (283, 172, 0), 2)


    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f"FPS: {int(fps)}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (283, 172, 0), 2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
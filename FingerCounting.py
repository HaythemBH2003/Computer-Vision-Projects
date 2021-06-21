import cv2
import time
import os
import HandTrackingModule as htm
import pyautogui as pg

previous_time = 0
camera_width, camera_height = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)

files = os.listdir("Images")
overlay_images = []
for finger_path in files:
    finger_image = cv2.imread(f"Images/{finger_path}")
    overlay_images.append(finger_image)

detector = htm.hand_detector(detection_confidence=0.75, track_confidence=0.75)

tipIds = [4, 8, 12, 16, 20]
x, y = 0, 0
while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)
    if len(lmList) > 0:
        fingers_open = []
        if lmList[4][1] < lmList[20][1]:
            if lmList[4][1] < lmList[3][1]:
                fingers_open.append(1)
            else:
                fingers_open.append(0)
        elif lmList[4][1] > lmList[20][1]:
            if lmList[4][1] < lmList[3][1]:
                fingers_open.append(0)
            else:
                fingers_open.append(1)
        if lmList[8][2] < lmList[6][2]:
            fingers_open.append(1)
        else:
            fingers_open.append(0)
        if lmList[12][2] < lmList[10][2]:
            fingers_open.append(1)
        else:
            fingers_open.append(0)
        if lmList[16][2] < lmList[14][2]:
            fingers_open.append(1)
        else:
            fingers_open.append(0)
        if lmList[20][2] < lmList[18][2]:
            fingers_open.append(1)
        else:
            fingers_open.append(0)
        
        try:
            total_fingers = fingers_open.count(1)
            img[0:200, 0:200] = overlay_images[total_fingers-1]
        except:
            pass

    current_time = time.time()
    try:
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, f"FPS: {int(fps)}", (40, 250), cv2.FONT_HERSHEY_PLAIN, 2, (283, 172, 0), 2)
    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)
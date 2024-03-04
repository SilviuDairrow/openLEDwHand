import cv2
import mediapipe as mp
import serial
import math

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
mpDraw_styles = mp.solutions.drawing_styles

arduino_port = 'COM4'
baud_rate = 9600

board = serial.Serial(arduino_port, baud_rate, timeout=1)

with mpHands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    try:
        while True:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            lmList = []

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    myHand = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHand.landmark):
                        h, w, c, = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])

            if len(lmList) != 0:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]

                cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)

                lungime = math.hypot(x2 - x1, y2 - y1)

                if (lungime >= 0) and (lungime <= 55):
                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    board.write("R".encode('utf-8'))

                elif (lungime >= 56) and (lungime <= 110):
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    board.write("G".encode('utf-8'))

                elif lungime >= 111:
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                    board.write("B".encode('utf-8'))

            cv2.imshow("Rex", img)
            cv2.waitKey(1)
            
    except KeyboardInterrupt:
        pass
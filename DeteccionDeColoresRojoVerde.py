import numpy as np
import cv2
import time
import serial

webcam = cv2.VideoCapture(0)
arduino = serial.Serial('/dev/ttyACM0', 9600)

while(1):
    
    _, frame = webcam.read()

    imageFrame = cv2.medianBlur(frame,25)
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([170, 70, 30], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    green_lower = np.array([70, 70, 30], np.uint8)
    green_upper = np.array([100, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    kernel = np.ones((5, 5), "uint8")
    
    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)
    
    green_mask = cv2.dilate(green_mask, kernel)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)

    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if(area > 30000):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))    
                cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)
                if (cX > 100):
                    comando = "rojo"
                    arduino.write(comando.encode())
                else:
                    comando = "siga"
                    arduino.write(comando.encode())

    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if(area > 30000):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                if (cX < 540):
                    comando = "verde"
                    arduino.write(comando.encode())
                else:
                    comando = "siga"
                    arduino.write(comando.encode())

    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

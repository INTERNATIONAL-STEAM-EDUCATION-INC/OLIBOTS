# Python code for Multiple Color Detection
# https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/


import numpy as np
import cv2
import mraa
import time

# Capturing video through webcam
webcam = cv2.VideoCapture(0)

gpio_1 = mraa.Gpio(23)
gpio_2 = mraa.Gpio(24)

gpio_1.dir(mraa.DIR_OUT)
gpio_2.dir(mraa.DIR_OUT)
time_ir = time.time()
time_ig = time.time()
# Start a while loop
while(1):
    
    # Reading the video from the
    # webcam in image frames
    _, frame = webcam.read()

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    imageFrame = cv2.medianBlur(frame,25)
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    red_lower = np.array([140, 40, 40], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
     # Set range for green color and
    # define mask
    green_lower = np.array([70, 60, 60], np.uint8)
    green_upper = np.array([100, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernel = np.ones((5, 5), "uint8")
    
    # For red color
    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)
    
    # For green color
    green_mask = cv2.dilate(green_mask, kernel)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        time_fr = time.time()
        time_tr = time_fr - time_ir
        if time_tr >= 1:
            gpio_2.write(0)
    else:
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 30000):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))    
                gpio_2.write(1)
                time_ir = time.time()
            else:
                time_fr = time.time()
                time_tr = time_fr - time_ir
                if time_tr >= 1:
                    gpio_2.write(0)
    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        time_fg = time.time()
        time_tg = time_fg - time_ig
        if time_tg >= 1:
            gpio_1.write(0)
    else:
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 30000):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                gpio_1.write(1)
            else:
                time_fg = time.time()
                time_tg = time_fr - time_ir
                if time_tg >= 1:
                    gpio_1.write(0)

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
        cap.release()
        cv2.destroyAllWindows()
        break

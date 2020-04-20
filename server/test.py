import numpy as np
import cv2

# Capture video from file
#cap = cv2.VideoCapture('D:/09d980032ed1.480.mp4')
cap = cv2.VideoCapture('src//assets//1.mp4')

while True:

    ret, frame = cap.read()

    if ret == True:



        cv2.imshow('frame',frame)


        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()

# your code goes here
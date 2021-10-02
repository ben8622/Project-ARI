import cv2 as cv
import numpy as np
import aruco_detect


ar = aruco_detect.aruco_detect()

frame1 = cv.imread("no_ar_present.png")
frame2 = cv.imread("boxesWithArucoTags.png")
ar_frame = ar.get_tags(frame2)

while(True):
    cv.imshow('ar test', ar_frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

print("DATA:")
print(ar.ar_counts)
print("Total Boxes: ", ar.total)
cv.destroyAllWindows()

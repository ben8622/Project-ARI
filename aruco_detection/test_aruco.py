import cv2 as cv
import numpy as np
import aruco_detect


ar = aruco_detect.aruco_detect()

frame1 = cv.imread("no_ar_present.png")
frame2 = cv.imread("boxesWithArucoTags.png")
frame3 = cv.imread("aruco_gate.png")


preview = True

if preview:
    ar_frame = ar.draw_tags_count(frame2)
else:
    g_check = ar.gate_check(frame2)
    if g_check:
        ar.count_tags(frame2)
        ar_frame = ar.draw_tags(frame2)
    else:
        ar_frame = frame2
    
while(True):
    cv.imshow('ar test', ar_frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

print("DATA:")
print(ar.ar_counts)
cv.destroyAllWindows()

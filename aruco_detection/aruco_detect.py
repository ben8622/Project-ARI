import cv2 as cv
import numpy as np

# Set up CV2 Aruco 
ar_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
ar_params = cv.aruco.DetectorParameters_create()

frame = cv.imread('boxesWithArucoTags.png')

ar_corners, ar_ids, rejects = cv.aruco.detectMarkers(frame, ar_dict, parameters=ar_params)

print(ar_ids)

total = np.sum(ar_ids)

print("Total Boxes: ", total)

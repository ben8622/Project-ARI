import cv2 as cv
import numpy as np

class aruco_detect:

    def __init__(self):
        # Set up CV2 Aruco 
        self.ar_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
        self.ar_params = cv.aruco.DetectorParameters_create()
        self.ar_counts = {}
        self.total = 0


    def get_tags(self, frame) -> dict:
        ar_corners, ar_ids, rejects = cv.aruco.detectMarkers(frame, self.ar_dict, parameters=self.ar_params)
        
        # Counts the number of each ar tag
        ar_set = set(ar_ids)
        self.ar_counts = dict((x, ar_ids.count(x) for x in ar_set))
        
        self.total = len(ar_ids)


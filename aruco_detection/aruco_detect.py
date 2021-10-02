import cv2 as cv
import numpy as np

class aruco_detect:

    def __init__(self):
        # Set up CV2 Aruco 
        self.ar_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
        self.ar_params = cv.aruco.DetectorParameters_create()
        self.ar_counts = {'0': 0, '1': 0, '2': 0}
        self.total = 0
        self.gate_no = np.array([10, 20, 30])
        for g in self.gate_no:
            self.gates = {g, False}
        

    def draw_tags(self, frame):
        # Detects AR tags
        ar_corn, ar_ids, rejects = cv.aruco.detectMarkers(frame, self.ar_dict, parameters=self.ar_params)
        
        if np.all(ar_ids == None):
            return(frame)
        else:
            # Draw border and label ar tags
            ar_frame = cv.aruco.drawDetectedMarkers(frame, ar_corn, ar_ids)
            return(ar_frame)
            
    
    def draw_tags_count(self, frame):
        # Detects AR tags
        ar_corn, ar_ids, rejects = cv.aruco.detectMarkers(frame, self.ar_dict, parameters=self.ar_params)
        
        if np.all(ar_ids == None):
            return(frame)
        else:
            self.count_tags(ar_ids)
            # Draw Outline around AR tags
            ar_frame = cv.aruco.drawDetectedMarkers(frame, ar_corn, ar_ids)
            return(ar_frame)


    def count_tags(self, ar_ids):
        # Counts the number of each ar tag
        unique, counts = np.unique(ar_ids, return_counts=True)
        self.ar_counts = dict(zip(unique.astype(str), counts))

        # Total number of tags/objects
        self.total = len(ar_ids)

import cv2 as cv
import numpy as np

class aruco_detect:

    def __init__(self):
        # Set up CV2 Aruco 
        self.ar_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
        self.ar_params = cv.aruco.DetectorParameters_create()
        self.ar_counts = {'0': 0, '1': 0, '2': 0}
        self.total = 0


    def get_tags(self, frame):
        # Detects AR tags
        ar_corn, ar_ids, rejects = cv.aruco.detectMarkers(frame, self.ar_dict, parameters=self.ar_params)
        self.ar_counts = {'0': 0, '1': 0, '2': 0}
        self.total = 0
        print(ar_corn)
        if np.all(ar_ids != None):

            # Tally total occurences of each tag
            for ar_id in ar_ids:
              self.ar_counts[str(ar_id[0])] = str(int(self.ar_counts[str(ar_id[0])]) + 1) 

            # Draw Outline around AR tags
            ar_frame = cv.aruco.drawDetectedMarkers(frame, ar_corn, ar_ids)
            
            return(ar_frame)
        else:
            return(frame)

    # def tag_distance(self, frame):            

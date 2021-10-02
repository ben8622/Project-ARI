import cv2 as cv
import numpy as np

class aruco_detect:

    def __init__(self):
        # Set up CV2 Aruco 
        self.ar_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
        self.ar_params = cv.aruco.DetectorParameters_create()
        self.ar_counts = {'0': 0, '1': 0, '2': 0}
        self.gate_no = np.array([10, 20, 30])
        self.size_of_frame = None
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
        self.ar_counts = {'0': 0, '1': 0, '2': 0}
        self.size_of_frame = frame.shape[0]
        if np.all(ar_ids == None):
            return(frame)
        else:
            self.count_tags(ar_ids, ar_corn)

            # Draw Outline around AR tags
            ar_frame = cv.aruco.drawDetectedMarkers(frame, ar_corn, ar_ids)
            return(ar_frame)

    def tag_distance(self, corner):
        corners_abcd = corner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners_abcd
        topRightPoint = (int(topRight[0]), int(topRight[1]))
        topLeftPoint = (int(topLeft[0]), int(topLeft[1]))
        bottomRightPoint = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeftPoint = (int(bottomLeft[0]), int(bottomLeft[1]))

        cX = int((topLeft[0] + bottomRight[0])//2)
        cY = int((topLeft[1] + bottomRight[1])//2)

        left_x, left_y = int(topLeft[0]), int(topLeft[1])
        right_x, right_y = int(topRight[0]), int(topRight[1])
        
        ## distance between top corners of detected ar tag IN THE IMG
        ed = (((left_x - right_x)**2 + (left_y - right_y)**2) ** 0.5) ## pixels
        ar_tag_width = 150 ## mm
        focal_length = 107.95 ## mm
        sensor_height = 70 # mm

        num = focal_length * ar_tag_width * self.size_of_frame
        denom = ed * sensor_height

        dist = ( num  / denom ) / 1000 # mm -> m

        print("distance = ", dist)

        return 0


    def count_tags(self, ar_ids, ar_corners):
        # Tally total occurences of each tag
        for (ar_id, corner) in zip(ar_ids, ar_corners):
            dist = self.tag_distance(corner)
            self.ar_counts[str(ar_id[0])] = str(int(self.ar_counts[str(ar_id[0])]) + 1) 


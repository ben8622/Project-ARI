import cv2 as cv
import numpy as np

class aruco_detect:

    def __init__(self):
        # Set up CV2 Aruco 
        self.ar_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
        self.ar_params = cv.aruco.DetectorParameters_create()
        self.ar_counts = {'0': 0, '1': 0, '2': 0, '10': 0, '20': 0, '30': 0}
        self.gate_no = np.array([10, 20, 30])
        self.size_of_frame = None
        self.scanning = False
        self.totals = {'0': 0, '1': 0, '2': 0, '10': 0, '20': 0, '30': 0}
        self.gates = {}
        for g in self.gate_no:
            self.gates.update({g: False})
        

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
        self.ar_counts = {'0': 0, '1': 0, '2': 0, '10': 0, '20': 0, '30': 0}
        self.size_of_frame = frame.shape[0]
        if np.all(ar_ids == None):
            return(frame)
        else:
            frame = self.count_tags(frame)
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
        sensor_height = 80 # mm

        num = focal_length * ar_tag_width * self.size_of_frame
        denom = ed * sensor_height

        dist = ( num  / denom ) / 1000 # mm -> m

        print("distance = ", dist)

        return dist, topLeft


    def gate_check(self, frame):
        # Width of camera frame
        w = frame.shape[1]
        
        # Detects AR tags
        ar_corn, ar_ids, rejects = cv.aruco.detectMarkers(frame, self.ar_dict, parameters=self.ar_params)

        # Check if gate tag is in view
        gate_found = False
        if np.all(ar_ids == None):
            return(False)
        else:
            ar_ids = ar_ids.flatten()
            for ar in ar_ids:
                if ar in self.gate_no and not self.gates[ar]:
                    i = np.where(ar_ids == ar)
                    i = i[0][0]
                    self.gates[ar] = True
                    gate_found = True
                else:
                    return(False)
            
        # Check if gate is in the center of view/screen
        gate_centered = False
        if gate_found:
            # Find center of of tag and its location on screen
            tlc = ar_corn[i][0][0]     # top left corner
            trc = ar_corn[i][0][1]     # top right corner
            print('width of frame: ',w)
            print('tlc ',tlc, 'trc: ',trc)
            # Location of the tag's center position on the screen
            tag_center_loc = 0.5*(trc[0] - tlc[0]) + tlc[0]
            print('center location: ', tag_center_loc)
            if 0.5*w - 50 <= tag_center_loc <= 0.5*w + 50 :
                return(True)
            else:
                return(False)
        else:
            return(False)
                

    def count_tags(self, frame):
        ar_corners, ar_ids, rejects = cv.aruco.detectMarkers(frame, self.ar_dict, parameters=self.ar_params)
        # Tally total occurences of each tag
        for (ar_id, corner) in zip(ar_ids, ar_corners):
            dist, topLeft = self.tag_distance(corner)
            frame = cv.putText(frame, str(dist), (int(topLeft[0]-10),   int(topLeft[1]-10)), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
            print(self.ar_counts)
            self.ar_counts[str(ar_id[0])] = str(int(self.ar_counts[str(ar_id[0])]) + 1) 

        return frame


    def reset_totals(self):
        self.totals = {'0': 0, '1': 0, '2': 0, '10': 0, '20': 0, '30': 0}


    def add2total(self):
        for x in self.ar_counts.keys():
            self.totals[x] += self.ar_counts[x]

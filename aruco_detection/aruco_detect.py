import cv2 as cv
import numpy as np

class aruco_detect:

    def __init__(self):
        # Set up CV2 Aruco 
        self.ar_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
        self.ar_params = cv.aruco.DetectorParameters_create()
        self.ar_counts = {'0': 0, '1': 0, '2': 0}
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
        self.ar_counts = {'0': 0, '1': 0, '2': 0}
        
        if np.all(ar_ids == None):
            return(frame)
        else:
            self.count_tags(ar_ids)

            # Draw Outline around AR tags
            ar_frame = cv.aruco.drawDetectedMarkers(frame, ar_corn, ar_ids)
            return(ar_frame)

    def tag_distance(self, corner): 
        Dist = []

        corners_abcd = corner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners_abcd
        topRightPoint = (int(topRight[0]), int(topRight[1]))
        topLeftPoint = (int(topLeft[0]), int(topLeft[1]))
        bottomRightPoint = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeftPoint = (int(bottomLeft[0]), int(bottomLeft[1]))

        cX = int((topLeft[0] + bottomRight[0])//2)
        cY = int((topLeft[1] + bottomRight[1])//2)

        measure = abs(3.5/(topLeft[0]-cX))
        #cv2.circle(image, (cX, cY), 4, (255, 0, 0), -1)
        #cv2.putText(image, str(int(markerId)), (int(topLeft[0]-10), int(topLeft[1]-10)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
        Dist.append((cX, cY))
        # print(arucoDict)
        if len(Dist) == 0:
            if Line_Pts is not None:
                Dist = Line_Pts
        if len(Dist) == 2:
            Line_Pts = Dist
        if len(Dist) == 2:
            #cv2.line(image, Dist[0], Dist[1], (255, 0, 255), 2)
            ed = ((Dist[0][0] - Dist[1][0])**2 +((Dist[0][1] - Dist[1][1])**2))**(0.5)
            #cv2.putText(image, str(int(measure*(ed))) + "cm", (int(300), int(300)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
            print("Euclidian distance = ", ed)


    def count_tags(self, ar_ids):
        # Tally total occurences of each tag
        for ar_id in ar_ids:
            self.ar_counts[str(ar_id[0])] = str(int(self.ar_counts[str(ar_id[0])]) + 1) 


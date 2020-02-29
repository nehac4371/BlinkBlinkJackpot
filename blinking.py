import cv2
import numpy as np
import dlib
import pandas as pd
import time
from math import hypot
import threading
#import slots as slt
import queue


close_it = False
#q_cnt = 0
q_val = False
q  = queue.Queue()

class CamTracker:

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    def __init__(self ): 
        self.pupil = []
        self.label = []
        self.timestamp = []
        self.blink_counter = 0
        self.q_cnt = 0 
        global q_val 
        global q
        #cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        
        self.cap = cv2.VideoCapture(0)
        #print('intialize Blink detection')
        self.recording = True
        global close_it
        
        
    
    def nothing(self):
        pass
    def midpoint(self,p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

    def get_blinking_ratio(self,eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = self.midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = self.midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))


        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

        ratio = hor_line_lenght / ver_line_lenght
        return ratio
    
    def start(self):
        k = 0
        while self.blink_counter < 3:
            #time.sleep(1)
            _, frame = self.cap.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #cv2.namedWindow('image',cv2.WINDOW_NORMAL)
            #cv2.imshow('image', frame)
            #key = cv2.waitKey(1)
            #height, width, _ = frame.shape
            faces,_,_ = self.detector.run(gray,0,0)
            if (len(faces)==1) :

                landmarks = self.predictor(gray, faces[0])
                #print(scores[i])
                left_eye_ratio = self.get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
                right_eye_ratio = self.get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
                blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

                if blinking_ratio > 5.7 and k>3:
                    k = 0
                    self.blink_counter+=1
                    q.put(self.blink_counter)
                    print("You blinked")
                    print(self.blink_counter)
                
                #q_val = False
                self.q_cnt =self.blink_counter
                #q.put(self.q_cnt)
            k+=1
            
        self.cap.release()
        cv2.destroyAllWindows()
        return self.pupil

#c = CamTracker()
#c.start()
        




#q = queue.Queue()

#t1.join()'''



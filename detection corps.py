# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:00:14 2023

@author: axelm
"""
import cv2 
import mediapipe as mp
import pyautogui
import time
import mss
import numpy as np
from math import sqrt

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
"""
with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 400, "height": 400}
    while "Screen capturing":
        end_time = time.time()
    
        # Get raw pixels from the screen, save it to a Numpy array
        frm = np.array(sct.grab(monitor))
        frm = cv2.flip(frm, 1)
        frame_rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
        
        _, frame = cap.read()
        
        pose_results = pose.process(frame_rgb)
        try: 
            print(sqrt(abs(pose_results.pose_landmarks.landmark[9].x-pose_results.pose_landmarks.landmark[10].x)**2+abs(pose_results.pose_landmarks.landmark[9].y-pose_results.pose_landmarks.landmark[10].y)**2+abs(pose_results.pose_landmarks.landmark[9].z-pose_results.pose_landmarks.landmark[10].z)**2))
            #print(abs(pose_results.pose_landmarks.landmark[9].x-pose_results.pose_landmarks.landmark[10].x))
        except:
            None
        
        # draw skeleton on the frame
        #mp_drawing.draw_landmarks(frm, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        cv2.imshow("window", frame)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            cap.release()
            break    
"""
while cap.isOpened():
    # read frame
    _, frame = cap.read()
    try:
         # resize the frame for portrait video
         # frame = cv2.resize(frame, (350, 600))
         # convert to RGB
         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         
         # process the frame for pose detection
         pose_results = pose.process(frame_rgb)
         try:
             print(sqrt(abs(pose_results.pose_landmarks.landmark[9].x-pose_results.pose_landmarks.landmark[10].x)**2+abs(pose_results.pose_landmarks.landmark[9].y-pose_results.pose_landmarks.landmark[10].y)**2+abs(pose_results.pose_landmarks.landmark[9].z-pose_results.pose_landmarks.landmark[10].z)**2))
         except:
             None
         #print(abs(pose_results.pose_landmarks.landmark[9].x-pose_results.pose_landmarks.landmark[10].x))
         
         # draw skeleton on the frame
         mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
         # display the frame
         cv2.imshow('Output', frame)
    except:
         break
    
    if cv2.waitKey(1) == ord('q'):
        break
          
cap.release()
cv2.destroyAllWindows()

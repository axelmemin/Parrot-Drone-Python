# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:41:10 2023

@author: axelm
"""

from pyparrot.Minidrone import Mambo
from pyparrot.DroneVisionGUI import DroneVisionGUI
import cv2
import mss
import numpy as np
import time
import mediapipe as mp
import random
from annexe import gauche, droite, haut, bas, avant, arriere, anim, rotation
from cv2 import aruco
from math import sqrt
from clap import *

# set this to true if you want to fly for the demo
testFlying = True

marker_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

param_markers = aruco.DetectorParameters_create()

jeu={'pierre':'feuille', 'feuille':'ciseaux', 'ciseaux':'pierre'}
obj=['pierre','feuille','ciseaux']
signe={2:'pierre',3:'feuille',4:'ciseaux'}

score=[0,0]

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        img = self.vision.get_latest_valid_picture()
        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            self.index +=1

def demo_mambo_user_vision_function(mamboVision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    mambo = args[0]
    b=True
    a=False
    if (testFlying):
        mambo.safe_takeoff(3)
        mambo.smart_sleep(1)
        mambo.flip(direction='back')
        mambo.smart_sleep(1)
        mambo.safe_land(3)
        """
        while b:
            aruc=[]
            vic=0
            #recherche audio clap qui synchronise les deux programmes
            tt = TapTester()
            while not a:
                a=tt.listen()
            drone=obj[random.randint(0,2)]
            print(drone)
            mambo.safe_takeoff(3)
            mambo.smart_sleep(1)
            bas(mambo,20)
            mambo.smart_sleep(1)
            if drone == 'pierre':
                avant(mambo,20)
                mambo.smart_sleep(3)
            if drone == 'feuille':
                gauche(mambo,20)
                mambo.smart_sleep(1)
                avant(mambo,20)
                mambo.smart_sleep(1)
            if drone == 'ciseaux':
                droite(mambo,20)
                mambo.smart_sleep(1)
                avant(mambo,20)
                mambo.smart_sleep(1)
            rotation(mambo,180)
            
            with mss.mss() as sct:
                # Part of the screen to capture
                monitor = {"top": 245, "left": 0, "width": 960, "height": 540}
                while "Screen capturing":
                    # Get raw pixels from the screen, save it to a Numpy array
                    imageFrame = np.array(sct.grab(monitor))
                    #filtre couleur pour interpretation
                    gray_frame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
                    #detection aruco marqueurs 
                    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
                    if marker_corners:
                        for i in range(len(marker_IDs)):
                            if marker_IDs[i] == 1:
                                for ids, corners in zip(marker_IDs, marker_corners):
                                    if ids == 1:
                                        corners = corners.reshape(4, 2)
                                        corners = corners.astype(int)
                                        top_right = corners[0].ravel()
                                        top_left = corners[1].ravel()
                                        bottom_right = corners[2].ravel()
                                        bottom_left = corners[3].ravel()
                                        width = (top_right[0]-top_left[0])*3
                                        mid = (top_right[0]+top_left[0])/2    
                                monitor1 = {"top": 245+max(bottom_right[1], bottom_left[1]), "left": int(mid-abs(width)), "width": int(abs(2*width)), "height": 1080}
                                imageFrame1 = np.array(sct.grab(monitor1))
                                cv2.imshow("frame1", imageFrame1)
                                gray_frame1 = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
                                marker_corners1, marker_IDs1, reject1 = aruco.detectMarkers(gray_frame1, marker_dict, parameters=param_markers)
                                if marker_corners1:
                                    for i in range(len(marker_IDs1)):
                                        if marker_IDs1[i] not in aruc and marker_IDs1[i]!=1:
                                            aruc.append(marker_IDs1[i])
                                            print(marker_IDs1[i])
                                    j=0
                                    while j < len(aruc):
                                        if aruc[j] not in marker_IDs1:
                                            aruc.remove(aruc[j])
                                        else: 
                                            j=j+1   
                                break
                    #cv2.imshow("frame", imageFrame)
                    if len(aruc)!=0:
                        break
                    if cv2.waitKey(1) == ord('q'):
                        break   
            cv2.destroyAllWindows()  
            print(drone)
            if jeu[drone]==signe[aruc[0][0]]:
                score[0]=score[0]+1
                print('drone adverse : '+signe[aruc[0][0]]) 
                print('drone : '+drone)
                print('drone adverse gagne')
                print(str(score[0])+' - '+str(score[1]))
                vic=2
            elif drone==signe[aruc[0][0]]:
                print('drone adverse : '+signe[aruc[0][0]])
                print('drone : '+drone)
                print('tie')
                print(str(score[0])+' - '+str(score[1]))
                vic=0
            elif jeu[signe[aruc[0][0]]]==drone:
                score[1]=score[1]+1
                print('drone adverse : '+signe[aruc[0][0]])
                print('drone : '+drone)
                print('drone adverse perd')
                print(str(score[0])+' - '+str(score[1]))
                vic=1
            #anim(vic, mambo)
            #mambo.smart_sleep(2)
            #mambo.safe_land(3)
            if input('nouvelle partie ? (oui/non)') == 'oui':
                b=True
            else:
                break
        print("Ending the sleep and vision")
        mamboVision.close_video()
        mambo.disconnect()
        mamboVision.vision_running = False
        mamboVision.close_exit()
        # done doing vision demo
        print("Ending the sleep and vision")
        mamboVision.close_video()
        """
    else:
        aruc=[]
        vic=0
        #recherche audio clap qui synchronise les deux programmes
        tt = TapTester()
        while not a:
            a=tt.listen()
        print('clap')
        with mss.mss() as sct:
            monitor = {"top": 245, "left": 960, "width": 960, "height": 540}
            while "Screen capturing":
                # Get raw pixels from the screen, save it to a Numpy array
                imageFrame = np.array(sct.grab(monitor))
                gray_frame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
                #detection aruco marqueurs 
                marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
                print(marker_IDs)
                cv2.imshow('frame',imageFrame)
                
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    break
        cv2.destroyAllWindows()
        print("Ending the sleep and vision")
        mamboVision.close_video()
        mambo.disconnect()
        mamboVision.vision_running = False
        mamboVision.close_exit()
        # done doing vision demo
        print("Ending the sleep and vision")
        mamboVision.close_video()
        
        print("disconnecting")
        mambo.disconnect()
        
wifi_ip='192.168.99.32'

if __name__ == "__main__":
    mamboAddr = "e0:14:d0:63:3d:d0"

    # make my mambo object
    mambo = Mambo(mamboAddr, use_wifi=True, wifi_ip=wifi_ip)
    print("trying to connect to mambo now")
    success = mambo.connect(num_retries=3)
    print("connected: %s" % success)

    if (success):
        # get the state information
        print("sleeping")
        mambo.smart_sleep(1)
        mambo.ask_for_state_update()
        mambo.smart_sleep(1)

        print("Preparing to open vision")
        #réalise tâche dicté par la fonction 'demo_mambo_user_vision_function' lorsque bouton vlc player 'run' actionné        
        mamboVision = DroneVisionGUI(mambo, is_bebop=False, buffer_size=200,
                                     user_code_to_run=demo_mambo_user_vision_function, user_args=(mambo, ),wifi_ip=wifi_ip)
        userVision = UserVision(mamboVision)
        mamboVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        mamboVision.open_video()
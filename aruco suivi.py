# -*- coding: utf-8 -*-
"""
Created on Mon May 22 09:59:02 2023

@author: axelm
"""

from pyparrot.Minidrone import Mambo
from pyparrot.DroneVisionGUI import DroneVisionGUI
import cv2
from cv2 import aruco
import mss
import numpy as np
from annexe import avant,arriere,gauche,droite
from math import sqrt

#differentes taches à réaliser suivant les marqueurs montrés
def instruc(aruc):
    for i in range(len(aruc)):
        if aruc[i]==42:
            mambo.flip(direction='back')
        if aruc[i]==27:
            mambo.flip(direction='front')
        if aruc[i]==43:
            mambo.turn_degrees(180)
            mambo.turn_degrees(180)
        if aruc[i]==18:
            mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=20, duration=1)
            mambo.smart_sleep(1)
            mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-20, duration=1)
        if aruc[i]==5:
            mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=1)
            mambo.smart_sleep(1)
            mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=1)
        mambo.smart_sleep(2)
            
    
#set this to true if you want to fly for the demo
testFlying = True
marker_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

param_markers = aruco.DetectorParameters_create()

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        # print("in save pictures on image %d " % self.index)

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
    top=[]
    dist=0
    if (testFlying):
        #tache réalisée si testFlying = True
        if (mambo.sensors.flying_state != "emergency"):
            #stockage différents marqueurs montrés
            print("taking off!")
            mambo.safe_takeoff(3)
            with mss.mss() as sct:
                # Part of the screen to capture
                monitor = {"top": 0, "left": 0, "width": 1920, "height": 880}
                while "Screen capturing":
                    # Get raw pixels from the screen, save it to a Numpy array
                    imageFrame = np.array(sct.grab(monitor))
                    #filtre couleur pour interpretation
                    gray_frame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
                    #detection aruco marqueurs 
                    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
                    if marker_corners:
                        for ids, corners in zip(marker_IDs, marker_corners):
                            cv2.polylines(imageFrame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA)
                            corners = corners.reshape(4, 2)
                            corners = corners.astype(int)
                            top_right = corners[0].ravel()
                            top_left = corners[1].ravel()
                            if top==[]:
                                top.append(top_right)
                                top.append(top_left)
                            bottom_right = corners[2].ravel()
                            bottom_left = corners[3].ravel()
                            cv2.putText(
                                imageFrame,
                                f"id: {ids[0]}",
                                top_right,
                                cv2.FONT_HERSHEY_PLAIN,
                                1.3,
                                (200, 100, 0),
                                2,
                                cv2.LINE_AA,
                            ) 
                            
                        if top != []:
                            dist=sqrt((top[0][0]-top[1][0])**2+(top[0][1]-top[1][1])**2)
                            dista=sqrt((top_left[0]-top_right[0])**2+(top_left[1]-top_right[1])**2)
                            milieu_x=(top[0][0]+top[1][0])/2
                            milieu_y=(top[0][1]+top[1][1])/2
                            x=(top_left[0]+top_right[0])/2
                            y=(top_left[1]+top_right[1])/2
                            if dista<dist*0.75:
                                print('trop loin')
                                avant(mambo,10)
                                mambo.smart_sleep(0.5)
                            elif dista>dist*1.25:
                                print('trop proche')
                                arriere(mambo,10)
                                mambo.smart_sleep(0.5)
                            else:
                                print('ok distance')
                            if x<milieu_x*0.75:
                                print('trop gauche')
                                gauche(mambo,10)
                                mambo.smart_sleep(0.5)
                            elif x>milieu_x*1.25:
                                print('trop droite')
                                droite(mambo,10)
                                mambo.smart_sleep(0.5)
                            else:
                                print('ok milieu')
                    
                    if cv2.waitKey(1) == ord('q'):
                        break
            
            mamboVision.vision_running = False
            mambo.disconnect()
            mamboVision.close_exit()
            cv2.destroyAllWindows()
    else:
        #tache réalisée si testFlying = False        
        ("Sleeeping for 15 seconds - move the mambo around")
        aruc=[]
        with mss.mss() as sct:
            # Part of the screen to capture
            monitor = {"top": 0, "left": 0, "width": 2000, "height": 2000}
            while "Screen capturing":            
                # Get raw pixels from the screen, save it to a Numpy array
                imageFrame = np.array(sct.grab(monitor))               
                gray_frame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
                marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
                if marker_corners:
                    for i in range(len(marker_IDs)):
                        if marker_IDs[i] not in aruc:
                            aruc.append(marker_IDs[i])
                            print(marker_IDs[i])
                    for ids, corners in zip(marker_IDs, marker_corners):
                        cv2.polylines(imageFrame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA)
                        corners = corners.reshape(4, 2)
                        corners = corners.astype(int)
                        top_right = corners[0].ravel()
                        top_left = corners[1].ravel()
                        bottom_right = corners[2].ravel()
                        bottom_left = corners[3].ravel()
                        cv2.putText(
                            imageFrame,
                            f"id: {ids[0]}",
                            top_right,
                            cv2.FONT_HERSHEY_PLAIN,
                            1.3,
                            (200, 100, 0),
                            2,
                            cv2.LINE_AA,
                        )
                if len(aruc)==3:
                    print(aruc)
                    aruc=[]
                # Program Termination
                if cv2.waitKey(1) == ord('q'):
                    break
        mamboVision.vision_running = False
        mambo.disconnect()
        mamboVision.close_exit()
        cv2.destroyAllWindows()

    # done doing vision demo
    print("Ending the sleep and vision")
    mamboVision.close_video()

    mambo.smart_sleep(5)

    print("disconnecting")
    mambo.disconnect()


if __name__ == "__main__":
    mamboAddr = "fe80::8469:b69f:b4b0:16bb%10"

    # make my mambo object
    mambo = Mambo(mamboAddr, use_wifi=True)
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
                                     user_code_to_run=demo_mambo_user_vision_function, user_args=(mambo, ))
        userVision = UserVision(mamboVision)
        mamboVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        mamboVision.open_video()
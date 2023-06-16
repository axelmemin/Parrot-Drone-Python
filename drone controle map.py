# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:43:35 2023

@author: axelm
"""
from pyparrot.Minidrone import Mambo
from pyparrot.DroneVisionGUI import DroneVisionGUI
#equivalent A* python
from implementation import *
import cv2
import pygame
from annexe import *
import mediapipe as mp
import mss
import time
import numpy as np

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

p=grille()

mamboAddr = "fe80::8469:b69f:b4b0:16bb%9"

# make my mambo object
mambo = Mambo(None, use_wifi=True)

print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

testFlying = True

def demo_mambo_user_vision_function(mamboVision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    mambo = args[0]

    if (testFlying):        
        if (mambo.sensors.flying_state != "emergency"):
            #mise en place detection main
            drawing = mp.solutions.drawing_utils
            hands = mp.solutions.hands
            hand_obj = hands.Hands(max_num_hands=1)
            start_init = False 
            prev = -1
            #stockage différents nombre de doigts montrés
            main=[]
            with mss.mss() as sct:
                # Part of the screen to capture
                monitor = {"top": 0, "left": 0, "width": 1920, "height": 880}
                main=[6]
                while "Screen capturing":
                    end_time = time.time()
                
                    # Get raw pixels from the screen, save it to a Numpy array
                    frm = np.array(sct.grab(monitor))
                    frm = cv2.flip(frm, 1)

                    #detection main
                    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

                    if res.multi_hand_landmarks:

                        hand_keyPoints = res.multi_hand_landmarks[0]

                        cnt = count_fingers(hand_keyPoints)

                        if not(prev==cnt):
                            if not(start_init):
                                start_time = time.time()
                                start_init = True

                            elif (end_time-start_time) > 1:
                                if (cnt == 1):
                                    print(1)
                                    main.append(1)
                                
                                elif (cnt == 2):
                                    print(2)
                                    main.append(2)

                                elif (cnt == 3):
                                    print(3)
                                    main.append(3)

                                elif (cnt == 4):
                                    print(4)
                                    main.append(4)

                                elif (cnt == 5):
                                    print(5)
                                    main.append(5)

                                prev = cnt
                                start_init = False
                    #si trois nombres montrés réaliser manipulation
                    if len(main)==p[-1]-1:
                        mambo.smart_sleep(2)
                        print("taking off!")
                        mambo.safe_takeoff(3)
                        
                        if (mambo.sensors.flying_state != "emergency"):
                            #il y aura ici le code permettant la capture video live de l'ecran ainsi que le moyen de detecter voulu
                            
                            print("flying state is %s" % mambo.sensors.flying_state)
                            mambo.smart_sleep(2)
                            
                            vol(p, main, mambo)

                            mambo.smart_sleep(2)
                            print("landing")
                            mambo.land()
                            mambo.safe_land(5)
                            print("flying state is %s" % mambo.sensors.flying_state)
                            mambo.smart_sleep(2)
                        main=[]
                        break

            mamboVision.vision_running = False
            mambo.disconnect()
            mamboVision.close_exit()
            cv2.destroyAllWindows()
    else:
        #tache réalisée si testFlying = False        
        with mss.mss() as sct:
            # Part of the screen to capture
            monitor = {"top": 100, "left": 50, "width": 2000, "height": 2000}
            drawing = mp.solutions.drawing_utils
            hands = mp.solutions.hands
            hand_obj = hands.Hands(max_num_hands=1)
            start_init = False 
            prev = -1
            main=[]
            while "Screen capturing":
                end_time = time.time()
            
                # Get raw pixels from the screen, save it to a Numpy array
                frm = np.array(sct.grab(monitor))
                frm = cv2.flip(frm, 1)

                res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

                if res.multi_hand_landmarks:

                    hand_keyPoints = res.multi_hand_landmarks[0]

                    cnt = count_fingers(hand_keyPoints)

                    if not(prev==cnt):
                        if not(start_init):
                            start_time = time.time()
                            start_init = True

                        elif (end_time-start_time) > 0.2:
                            if (cnt == 1):
                                print(1)
                                main.append(1)
                            
                            elif (cnt == 2):
                                print(2)
                                main.append(2)

                            elif (cnt == 3):
                                print(3)
                                main.append(3)

                            elif (cnt == 4):
                                print(4)
                                main.append(4)

                            elif (cnt == 5):
                                print(5)
                                main.append(5)

                            prev = cnt
                            start_init = False
                if len(main)==3:
                    print(main)
                    main=[]

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
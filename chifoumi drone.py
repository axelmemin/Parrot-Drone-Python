# -*- coding: utf-8 -*-
"""
Created on Fri May  5 13:54:58 2023

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

jeu={'pierre':'feuille', 'feuille':'ciseaux', 'ciseaux':'pierre'}
obj=['pierre','feuille','ciseaux']

# set this to true if you want to fly for the demo
testFlying = False

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        img = self.vision.get_latest_valid_picture()
        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            self.index +=1

#comptage de doigts par comparaison de distance entre les différents points placés sur la main
def count_fingers(lst):
    cnt = 0

    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 6:
        cnt += 1
        
    return cnt 


def demo_mambo_user_vision_function(mamboVision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    mambo = args[0]

    if (testFlying):
        #tache réalisée si testFlying = True        
        if (mambo.sensors.flying_state != "emergency"):
            q=None
            compte=[]
            score=[0,0]
            while q!=[4,5,4]:
                choix=None
                cap = cv2.VideoCapture(0)
                drawing = mp.solutions.drawing_utils
                hands = mp.solutions.hands
                hand_obj = hands.Hands(max_num_hands=1)
                start_init = False 
                prev = -1
                while True:
                    with mss.mss() as sct:
                        # Part of the screen to capture
                        monitor = {"top": 0, "left": 0, "width": 2000, "height": 2000}
                        while "Screen capturing":
                            end_time = time.time()
                        
                            # Get raw pixels from the screen, save it to a Numpy array
                            frm = np.array(sct.grab(monitor))
                            frm = cv2.flip(frm, 1)
                            
                            res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

                            if res.multi_hand_landmarks:

                                hand_keyPoints = res.multi_hand_landmarks[0]

                                cnt = count_fingers(hand_keyPoints)

                                if compte==[3,2,1]:
                                    if not(prev==cnt):
                                        if not(start_init):
                                            start_time = time.time()
                                            start_init = True

                                        elif (end_time-start_time) > 1:
                                            if (cnt == 0):
                                                compte=[]
                                                choix='pierre'
                                                cv2.destroyAllWindows()
                                                cap.release()
                                                break
                                            elif (cnt == 2):
                                                compte=[]
                                                choix='ciseaux' 
                                                cv2.destroyAllWindows()
                                                cap.release()
                                                break
                                            elif (cnt == 5):
                                                compte=[]
                                                choix='feuille'
                                                cv2.destroyAllWindows()
                                                cap.release()
                                                break
                                            prev = cnt
                                            start_init = False                                
                                if not(prev==cnt) and compte!=[3,2,1]:
                                    if not(start_init):
                                        start_time = time.time()
                                        start_init = True
                                    elif (end_time-start_time) > 0.5:
                                        if (cnt == 3) and compte==[]:
                                            compte.append(3)
                                            print(compte)
                                        elif (cnt == 2) and compte==[3]:
                                            compte.append(2)
                                            print(compte)
                                        elif (cnt == 1) and compte==[3,2]:
                                            compte.append(1)
                                            print(compte)
                                        if (cnt == 4) and (q==[] or q==[4,5]):
                                            q.append(4)
                                        elif (cnt == 5) and q==[4]:
                                            q.append(5)
                                        prev = cnt
                                        start_init = False                                
                            if cv2.waitKey(1) == ord('q'):
                                cv2.destroyAllWindows()
                                cap.release()
                                break
                        drone=obj[random.randint(0,2)]
                        if jeu[drone]==choix:
                            score[0]=score[0]+1
                            print(choix) 
                            print(drone)
                            print('you won')
                            print(str(score[0])+' - '+str(score[1]))
                        elif drone==choix:
                            print(choix)
                            print(drone)
                            print('tie')
                            print(str(score[0])+' - '+str(score[1]))
                        elif jeu[choix]==drone:
                            score[1]=score[1]+1
                            print(choix)
                            print(drone)
                            print('you loose')
                            print(str(score[0])+' - '+str(score[1]))
            print("landing")
            print("flying state is %s" % mambo.sensors.flying_state)
            mambo.safe_land(5)

            mamboVision.vision_running = False
            mambo.disconnect()
            mamboVision.close_exit()
            cv2.destroyAllWindows()
    else:
        if (mambo.sensors.flying_state != "emergency"):
            q=None
            compte=[]
            score=[0,0]
            while q!=[4,5,4]:
                choix=None
                cap = cv2.VideoCapture(0)
                drawing = mp.solutions.drawing_utils
                hands = mp.solutions.hands
                hand_obj = hands.Hands(max_num_hands=1)
                start_init = False 
                prev = -1
                while True:
                    with mss.mss() as sct:
                        # Part of the screen to capture
                        monitor = {"top": 0, "left": 0, "width": 2000, "height": 2000}
                        while "Screen capturing":
                            end_time = time.time()
                        
                            # Get raw pixels from the screen, save it to a Numpy array
                            frm = np.array(sct.grab(monitor))
                            frm = cv2.flip(frm, 1)
                            
                            res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

                            if res.multi_hand_landmarks:

                                hand_keyPoints = res.multi_hand_landmarks[0]

                                cnt = count_fingers(hand_keyPoints)

                                if compte==[3,2,1]:
                                    if not(prev==cnt):
                                        if not(start_init):
                                            start_time = time.time()
                                            start_init = True

                                        elif (end_time-start_time) > 1:
                                            if (cnt == 0):
                                                compte=[]
                                                choix='pierre'
                                                cv2.destroyAllWindows()
                                                cap.release()
                                                break
                                            elif (cnt == 2):
                                                compte=[]
                                                choix='ciseaux' 
                                                cv2.destroyAllWindows()
                                                cap.release()
                                                break
                                            elif (cnt == 5):
                                                compte=[]
                                                choix='feuille'
                                                cv2.destroyAllWindows()
                                                cap.release()
                                                break
                                            prev = cnt
                                            start_init = False
                                
                                if not(prev==cnt) and compte!=[3,2,1]:
                                    if not(start_init):
                                        start_time = time.time()
                                        start_init = True
                                    elif (end_time-start_time) > 0.5:
                                        if (cnt == 3) and compte==[]:
                                            compte.append(3)
                                            print(compte)
                                        elif (cnt == 2) and compte==[3]:
                                            compte.append(2)
                                            print(compte)
                                        elif (cnt == 1) and compte==[3,2]:
                                            compte.append(1)
                                            print(compte)
                                        if (cnt == 4) and (q==[] or q==[4,5]):
                                            q.append(4)
                                        elif (cnt == 5) and q==[4]:
                                            q.append(5)
                                        prev = cnt
                                        start_init = False                                
                            if cv2.waitKey(1) == ord('q'):
                                cv2.destroyAllWindows()
                                cap.release()
                                break
                        drone=obj[random.randint(0,2)]
                        if jeu[drone]==choix:
                            score[0]=score[0]+1
                            print(choix) 
                            print(drone)
                            print('you won')
                            print(str(score[0])+' - '+str(score[1]))
                        elif drone==choix:
                            print(choix)
                            print(drone)
                            print('tie')
                            print(str(score[0])+' - '+str(score[1]))
                        elif jeu[choix]==drone:
                            score[1]=score[1]+1
                            print(choix)
                            print(drone)
                            print('you loose')
                            print(str(score[0])+' - '+str(score[1]))

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
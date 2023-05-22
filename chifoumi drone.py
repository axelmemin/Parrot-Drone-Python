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
from annexe import gauche, droite, haut, bas, avant, arriere, anim
from cv2 import aruco
from math import sqrt


jeu={'pierre':'feuille', 'feuille':'ciseaux', 'ciseaux':'pierre'}
obj=['pierre','feuille','ciseaux']

# set this to true if you want to fly for the demo
testFlying = True

marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

param_markers = aruco.DetectorParameters_create()

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
    top=[]
    dist=0

    if (testFlying):
        print("taking off!")
        mambo.safe_takeoff(5)
        #tache réalisée si testFlying = True        
        if (mambo.sensors.flying_state != "emergency"):
            q=[]
            score=[0,0]
            drawing = mp.solutions.drawing_utils
            hands = mp.solutions.hands
            hand_obj = hands.Hands(max_num_hands=1)
            start_init = False 
            prev = -1
            while q!=[4,5,4]:
                compte=[]
                choix=None
                x=None
                y=None
                while True and q!=[4,3,4]:
                    with mss.mss() as sct:
                        # Part of the screen to capture
                        monitor = {"top": 0, "left": 0, "width": 2000, "height": 2000}
                        while "Screen capturing":
                            end_time = time.time()
                        
                            # Get raw pixels from the screen, save it to a Numpy array
                            frm = np.array(sct.grab(monitor))
                            
                            gray_frame = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

                            frm = cv2.flip(frm, 1)
                            
                            marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
                            if marker_corners:
                                for ids, corners in zip(marker_IDs, marker_corners):
                                    cv2.polylines(frm, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA)
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
                                        frm,
                                        f"id: {ids[0]}",
                                        top_right,
                                        cv2.FONT_HERSHEY_PLAIN,
                                        1.3,
                                        (200, 100, 0),
                                        2,
                                        cv2.LINE_AA,
                                    ) 
                                    
                                if top != []:
                                    dist=sqrt((top[0][0]-top[1][0])**2-(top[0][1]-top[1][1])**2)
                                    dista=sqrt((top_left[0]-top_right[0])**2-(top_left[1]-top_right[1])**2)
                                    milieu_x=(top[0][0]+top[1][0])/2
                                    milieu_y=(top[0][1]+top[1][1])/2
                                    x=(top_left[0]+top_right[0])/2
                                    y=(top_left[1]+top_right[1])/2
                                    if dista<dist*0.75:
                                        print('trop loin')
                                        avant(mambo,10)
                                    elif dista>dist*1.25:
                                        print('trop proche')
                                        arriere(mambo,10)
                                    else:
                                        print('ok distance')
                                    if x<milieu_x*0.75:
                                        print('trop gauche')
                                        droite(mambo,10)
                                    elif x>milieu_x*1.25:
                                        print('trop droite')
                                        gauche(mambo,10)
                                    else:
                                        print('ok milieu')
                            
                            res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

                            if res.multi_hand_landmarks:

                                hand_keyPoints = res.multi_hand_landmarks[0]

                                cnt = count_fingers(hand_keyPoints)

                                if compte==[3,2,1]:
                                    if not(prev==cnt):
                                        if not(start_init):
                                            start_time = time.time()
                                            start_init = True

                                        elif (end_time-start_time) > 0.7:
                                            if (cnt == 0):
                                                compte=[]
                                                choix='pierre'
                                                break
                                            elif (cnt == 2):
                                                compte=[]
                                                choix='ciseaux' 
                                                break
                                            elif (cnt == 5 or cnt == 4):
                                                compte=[]
                                                choix='feuille'
                                                break
                                            prev = cnt
                                            start_init = False  
                                            
                                if not(prev==cnt) and compte!=[3,2,1]:
                                    if not(start_init):
                                        start_time = time.time()
                                        start_init = True
                                    elif (end_time-start_time) > 0.3:
                                        if (cnt == 3) and compte==[]:
                                            compte.append(3)
                                            print(compte)
                                        elif (cnt == 2) and compte==[3]:
                                            compte.append(2)
                                            print(compte)
                                        elif (cnt == 1) and compte==[3,2]:
                                            compte.append(1)
                                            print(compte)
                                        if (cnt == 4) and (q==[] or q==[4,3]):
                                            q.append(4)
                                            print(q)
                                        elif (cnt == 3) and q==[4]:
                                            q.append(3)
                                            print(q)
                                        prev = cnt
                                        start_init = False
                                """
                                for i in range(21):
                                    if hand_keyPoints.landmark[i].x*100 < 20 :
                                        x=1
                                    elif hand_keyPoints.landmark[i].x*100 > 80 :
                                        x=2
                                    else:
                                        x=0
                                    if hand_keyPoints.landmark[i].y*100 < 20 :
                                        y=1
                                    elif hand_keyPoints.landmark[i].y*100 > 80 :
                                        y=2
                                    else:
                                        y=0
                               
                            if x==1:
                                droite(mambo)
                            elif x==2:
                                gauche(mambo)
                            if y==1:
                                haut(mambo)
                            elif y==2:
                                bas(mambo)
                            """    
                            if q==[4,3,4]:
                                cv2.destroyAllWindows()
                                break
                        if q==[4,3,4]:
                            break    
                        drone=obj[random.randint(0,2)]
                        vic=0
                        if jeu[drone]==choix:
                            score[0]=score[0]+1
                            print(choix) 
                            print(drone)
                            print('you won')
                            print(str(score[0])+' - '+str(score[1]))
                            vic=1
                        elif drone==choix:
                            print(choix)
                            print(drone)
                            print('tie')
                            print(str(score[0])+' - '+str(score[1]))
                            vic=0
                        elif jeu[choix]==drone:
                            score[1]=score[1]+1
                            print(choix)
                            print(drone)
                            print('you loose')
                            print(str(score[0])+' - '+str(score[1]))
                            vic=2
                        if drone == 'pierre':
                            avant(mambo,20)
                            mambo.smart_sleep(2)
                            anim(vic, mambo)
                            mambo.smart_sleep(2)
                            arriere(mambo,20)
                            break
                        elif drone== 'ciseaux':
                            gauche(mambo,20)
                            mambo.smart_sleep(2)
                            anim(vic, mambo)
                            mambo.smart_sleep(2)
                            droite(mambo,20)
                            break
                        else:
                            droite(mambo,20)
                            mambo.smart_sleep(2)
                            anim(vic, mambo)
                            mambo.smart_sleep(2)
                            gauche(mambo,20)
                            break
                q=[]
            print("landing")
            print("flying state is %s" % mambo.sensors.flying_state)
            mambo.land(5)
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
                drawing = mp.solutions.drawing_utils
                hands = mp.solutions.hands
                hand_obj = hands.Hands(max_num_hands=1)
                start_init = False 
                prev = -1
                x=None
                y=None
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
                                                break
                                            elif (cnt == 2):
                                                compte=[]
                                                choix='ciseaux' 
                                                cv2.destroyAllWindows()
                                                break
                                            elif (cnt == 5 or cnt == 4):
                                                compte=[]
                                                choix='feuille'
                                                cv2.destroyAllWindows()
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
                                        
                                for i in range(21):
                                    if hand_keyPoints.landmark[i].x*100 < 20 :
                                        x=1
                                    elif hand_keyPoints.landmark[i].x*100 > 80 :
                                        x=2
                                    else:
                                        x=0
                                    if hand_keyPoints.landmark[i].y*100 < 20 :
                                        y=1
                                    elif hand_keyPoints.landmark[i].y*100 > 80 :
                                        y=2
                                    else:
                                        y=0
                                
                            if x==1:
                                print('dehors gauche')
                            elif x==2:
                                print('dehors droite')
                            if y==1:
                                print('dehors haut')
                            elif y==2:
                                print('dehors bas')
                                                            
                            if cv2.waitKey(1) == ord('q'):
                                cv2.destroyAllWindows()
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
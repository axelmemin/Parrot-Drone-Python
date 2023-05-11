# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:16:36 2023

@author: axelm
"""

import cv2 
import mediapipe as mp
import pyautogui
import time
import random

jeu={'pierre':'feuille', 'feuille':'ciseaux', 'ciseaux':'pierre'}
obj=['pierre','feuille','ciseaux']

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

q=input('Appuie sur entree pour commencer, ecrit "stop" pour arreter ')
print('faire decompte de 3 à 1 avec les doigts puis signe choisi')
score=[0,0]
compte=[]

while q!='stop':
    choix=None
    cap = cv2.VideoCapture(0)
    drawing = mp.solutions.drawing_utils
    hands = mp.solutions.hands
    hand_obj = hands.Hands(max_num_hands=1)
    start_init = False 
    prev = -1
    while True:
        end_time = time.time()
        _, frm = cap.read()
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
                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)
            
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
                    prev = cnt
                    start_init = False
            drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

        cv2.imshow("window", frm)

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
    q=input('Appuie sur entree pour recommencer, ecrit "stop" pour arreter ')

    
    


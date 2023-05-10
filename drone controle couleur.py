# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:34:23 2023

@author: axelm
"""

from pyparrot.Minidrone import Mambo
from pyparrot.DroneVisionGUI import DroneVisionGUI
import cv2
import mss
import numpy as np
import time

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


def demo_mambo_user_vision_function(mamboVision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    mambo = args[0]

    if (testFlying):
        print("taking off!")
        mambo.safe_takeoff(5)

        if (mambo.sensors.flying_state != "emergency"):
            c=[]
            with mss.mss() as sct:
                # Part of the screen to capture
                monitor = {"top": 0, "left": 0, "width": 2000, "height": 2000}
                while "Screen capturing":                
                    # Get raw pixels from the screen, save it to a Numpy array
                    imageFrame = np.array(sct.grab(monitor))
                   
                    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
                  
                    # Set range for red color and 
                    # define mask
                    red_lower = np.array([136, 87, 111], np.uint8)
                    red_upper = np.array([180, 255, 255], np.uint8)
                    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
                      
                    # Morphological Transform, Dilation
                    # for each color and bitwise_and operator
                    # between imageFrame and mask determines
                    # to detect only that particular color
                    kernel = np.ones((5, 5), "uint8")
                      
                    # For red color
                    red_mask = cv2.dilate(red_mask, kernel)
                    res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                              mask = red_mask)
                      
                    # Creating contour to track red color
                    contours, hierarchy = cv2.findContours(red_mask,
                                                           cv2.RETR_TREE,
                                                           cv2.CHAIN_APPROX_SIMPLE)
                    i=0  
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if(area > 300):
                            i=i+1
                            if i not in c:
                                mambo.turn_degrees(180)
                                time.sleep(1)
                                c.append(i)
                                print('R')
                                print(c)
                            while i < c[-1]:
                                del(c[-1])
                            x, y, w, h = cv2.boundingRect(contour)
                            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                                       (x + w, y + h), 
                                                       (0, 0, 255), 2)
                              
                            cv2.putText(imageFrame, "Red Colour"+str(i), (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                        (0, 0, 255))    
                        if i==0:
                            c=[]
                    if cv2.waitKey(1) == ord('q'):
                        break
            cv2.destroyAllWindows()
            mamboVision.close_exit()
        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
    else:
        print("Sleeeping for 15 seconds - move the mambo around")
        #stockage zone couleur actuellement visible par la camera live du drone
        c=[]
        with mss.mss() as sct:
            # Part of the screen to capture
            monitor = {"top": 0, "left": 0, "width": 2000, "height": 2000}
            while "Screen capturing":           
                # Get raw pixels from the screen, save it to a Numpy array
                imageFrame = np.array(sct.grab(monitor))
            
                hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
              
                # Set range for red color and 
                # define mask
                red_lower = np.array([136, 87, 111], np.uint8)
                red_upper = np.array([180, 255, 255], np.uint8)
                red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
                  
                # Morphological Transform, Dilation
                # for each color and bitwise_and operator
                # between imageFrame and mask determines
                # to detect only that particular color
                kernel = np.ones((5, 5), "uint8")
                  
                # For red color
                red_mask = cv2.dilate(red_mask, kernel)
                res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                          mask = red_mask)
                  
                # Creating contour to track red color
                contours, hierarchy = cv2.findContours(red_mask,
                                                       cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)
                i=0  
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    #consideration des zones de couleurs uniquement d'une certaine taille à ajuster suivant 
                    #taille de nos cartons rouges et distance à laquelle on veut les reconnaitre  
                    if(area > 300):
                        i=i+1
                        #exemple tache à realiser lorsque interprete zone rouge
                        if i not in c:
                            mambo.turn_degrees(180)
                            time.sleep(1)
                            c.append(i)
                            print('R')
                            print(c)
                        #garde en memoire zones rouges deja interpretées autrement interprète 
                        #continuellement comme nouvelle zone de couleur
                        while i < c[-1]:
                            del(c[-1])
                        x, y, w, h = cv2.boundingRect(contour)
                        imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                                   (x + w, y + h), 
                                                   (0, 0, 255), 2)
                          
                        cv2.putText(imageFrame, "Red Colour"+str(i), (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                    (0, 0, 255))    
                    if i==0:
                        c=[]
                if cv2.waitKey(1) == ord('q'):
                    break
        cv2.destroyAllWindows()
        mamboVision.close_exit()

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
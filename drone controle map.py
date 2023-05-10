# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:13:45 2023

@author: axelm
"""

from pyparrot.Minidrone import Mambo
#equivalent A* python
from implementation import *
import cv2
#OCR reconnaissance écriture
import pytesseract

#variable str contenant texte lu
texte=''

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#lecture image contenant le texte représentant la carte
img = cv2.imread("C:/Users/axelm/OneDrive/Bureau/drone stage/sample8.png")

#filtre couleur pour interpretation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
												cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = img.copy()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
	x, y, w, h = cv2.boundingRect(cnt)
	
	# Drawing a rectangle on copied image
	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	# Cropping the text block for giving input to OCR
	cropped = im2[y:y + h, x:x + w]
	
	# Apply OCR on the cropped image
	text = pytesseract.image_to_string(cropped)

    #ajout texte lu sur partie image au texte global
	texte=texte+text+'\n'

#'a'=point normal carte
#'bb'=obstacle
#'A'=départ
#'Z'=objectif
#'K','L','M'=emplacements manipulations à réaliser
print(texte)

#liste de listes representant les colonnes et lignes de la carte
graph=[]
i=0
#liste temporaire pour stocker une ligne de la carte
temp=[]
#boucle permettant de transcrire le texte str de la carte en une liste de lignes
while i != len(texte):
    #ajout element meme ligne dans liste 'temp'
    while texte[i] != '\n' :
        temp.append(texte[i])
        #gestion cas 'out of range' 
        if i+1 <= len(texte):   
            i=i+1
        else:
            break
    #retire listes vides sans interet
    if temp != list():
        graph.append(temp)
    temp=[]
    #gestion cas 'out of range'
    if i+1 <= len(texte):   
        i=i+1
    else:
        break

#obstacle occupe espace de deux points 
#rassemble les 'b' cote à cote pour représenter un unique obstacle
for i in range(len(graph)):
    j=0
    while j < len(graph[0]):
        if graph[i][j]=='b':
            graph[i][j]='bb'
            del(graph[i][j+1])
        j=j+1

#recupere les coordonnées des obstacles sous forme de listes
def mur(graph):
    coord=[]
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j]=='bb':
                coord.append((j,i))
    return coord

#recupere les coordonnées du point de départ
def start(graph):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j]=='A':
                return(j,i)

#recupere les coordonnées du point d'objectif            
def goal(graph):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j]=='Z':
                return(j,i)
            
#recupere les dimensions de la carte donnée            
def taille(graph):
    return (len(graph[0]),len(graph))

#recupere les coordonnées du point de la premiere manipulation
def manip1(graph):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j]=='K':
                return(j,i)

#recupere les coordonnées du point de la deuxieme manipulation            
def manip2(graph):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j]=='L':
                return(j,i)

#recupere les coordonnées du point de la troisieme manipulation            
def manip3(graph):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j]=='M':
                return(j,i)

#stockage sous forme variable des différents points de passage 
#pour réalisations des différents trajets                
start1=start(graph)
start2=manip1(graph)
start3=manip2(graph)
start4=manip3(graph)
goal1=manip1(graph)
goal2=manip2(graph)
goal3=manip3(graph)
goal4=goal(graph)

x,y=taille(graph)

#création graphe
diagram = GridWithWeights(x,y)
diagram.walls = mur(graph)

#stockage des différents trajets optimisés par A* pour chaque point de départ et d'arrivé
came_from, cost_so_far = a_star_search(diagram, start1, goal4)    
came_from1, cost_so_far1 = a_star_search(diagram, start1, goal1)
came_from2, cost_so_far2 = a_star_search(diagram, start2, goal2)
came_from3, cost_so_far3 = a_star_search(diagram, start3, goal3)
came_from4, cost_so_far4 = a_star_search(diagram, start4, goal4)

#affichage des différents graphes et des trajets
draw_grid(diagram, point_to=came_from, start=start, goal=goal)
print()
draw_grid(diagram, path=reconstruct_path(came_from1, start=start1, goal=goal1))
print()
draw_grid(diagram, path=reconstruct_path(came_from2, start=start2, goal=goal2))
print()
draw_grid(diagram, path=reconstruct_path(came_from3, start=start3, goal=goal3))
print()
draw_grid(diagram, path=reconstruct_path(came_from4, start=start4, goal=goal4))

#fonction permettant de réaliser avec une certaine precision une distance donnée avec le drone
def dist(di):
    d=0
    t0=0
    while d<di:
        #petit déplacement du drone 
        mambo.fly_direct(roll=0, pitch=25, yaw=0, vertical_movement=0, duration=0.1)
        #recuperation vitesse avancée drone
        v=mambo.sensors.speed_x
        #recuperation temps vol relié à vitesse récuperée + conversion en s
        t=mambo.sensors.speed_ts()/1000
        #ajout à distance global distance parcouru durant dernier deplacement
        d=d+v*(t-t0)
        #remise à niveau du temps de vol en mouvement
        t0=mambo.sensors.speed_ts()/1000
        mambo.smart_sleep(0.4)

#fonction permettant au drone de réaliser le trajet suivant la carte donnée
#angles rotation à revoir suivant orientation interpretation carte
def carte(path, di):
    #variable stockant orientation drone
    a=0
    for i in range(len(path)-1):
        #cas meme ligne
        if path[i][0]==path[i+1][0]:
            #comparaison coordonnée colonne pour savoir rotation gauche ou droite
            if path[i][1]==path[i+1][1]:
                mambo.turn_degrees(90)
                a=90
                dist(di)
            else:
                mambo.turn_degrees(-90)
                a=-90
                dist(di)
        
        #cas ligne différente
        else:
            #comparaison coordonnée ligne pour savoir rotation gauche ou droite            
            if path[i][0]==path[i+1][0]+1:
                #rotation suivant orientation drone
                if a==90:
                    mambo.turn_degrees(-90)
                    a=0
                    dist(di)
                elif a==-90:
                    mambo.turn_degrees(90)
                    a=0
                    dist(di)
                elif a==0:
                    dist(di)
            else:
                mambo.turn_degrees(180)
                dist(di)

#stockage manipulation à réaliser aux points de manipulation 
#manip sera determiné par interpretation video live avec detection couleur, marqueur aruco ou signe main
manip=[]

mamboAddr = "fe80::8469:b69f:b4b0:16bb%9"

# make my mambo object
mambo = Mambo(None, use_wifi=True)

print("trying to connect")
#success = mambo.connect(num_retries=3)
print("connected: %s" % success)

#definition des mouvements élementaires du drone
def avant():
    mambo.fly_direct(roll=0, pitch=25, yaw=0, vertical_movement=0, duration=0.1)
        
def arriere():
    mambo.fly_direct(roll=0, pitch=25, yaw=0, vertical_movement=0, duration=0.1)
    
def gauche():
    mambo.fly_direct(roll=-25, pitch=0, yaw=0, vertical_movement=0, duration=0.1)
    
def droite():
    mambo.fly_direct(roll=-25, pitch=0, yaw=0, vertical_movement=0, duration=0.1)

def diago_avant():
        mambo.fly_direct(roll=30, pitch=30, yaw=0, vertical_movement=0, duration=0.1)

def diago_arriere():
        mambo.fly_direct(roll=30, pitch=-30, yaw=0, vertical_movement=0, duration=0.1)

def rotation(deg):
        mambo.turn_degrees(deg)

testFlying = False

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
            #il y aura ici le code permettant la capture video live de l'ecran ainsi que le moyen de detecter voulu
            print("taking off!")
            mambo.safe_takeoff(5)
            
            print("flying state is %s" % mambo.sensors.flying_state)
            mambo.smart_sleep(2)
            
            #trajet du point de départ au lieu de la premiere manipulation
            carte(reconstruct_path(came_from1, start=start1, goal=goal1), dist)
            mambo.smart_sleep(1)
            #realisation premiere manipulation
            instruc(manip[0])
            
            #trajet du lieu de la premiere manipulation au lieu de la deuxieme manipulation
            carte(reconstruct_path(came_from2, start=start2, goal=goal2), dist)
            mambo.smart_sleep(1)
            #realisation deuxieme manipulation        
            instruc(manip[1])

            #trajet du lieu de la deuxieme manipulation au lieu de la troisieme manipulation        
            carte(reconstruct_path(came_from3, start=start3, goal=goal3), dist)
            mambo.smart_sleep(1)
            #realisation troisieme manipulation
            instruc(manip[2])
            
            #trajet du lieu de la troisieme manipulation au point d'arrivé
            carte(reconstruct_path(came_from4, start=start4, goal=goal4), dist)

            mambo.smart_sleep(2)
            print("landing")
            mambo.safe_land(5)
            print("flying state is %s" % mambo.sensors.flying_state)
            mambo.smart_sleep(2)
                

            print("disconnect")
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
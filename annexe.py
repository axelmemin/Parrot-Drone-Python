# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:40:47 2023

@author: axelm
"""
from pyparrot.Minidrone import Mambo
#equivalent A* python
from implementation import *
import cv2
import pygame


#definition des mouvements élementaires du drone
def avant(mambo, puiss):
    mambo.fly_direct(roll=0, pitch=puiss, yaw=0, vertical_movement=0, duration=0.1)
        
def arriere(mambo, puiss):
    mambo.fly_direct(roll=0, pitch=-puiss, yaw=0, vertical_movement=0, duration=0.1)
    
def gauche(mambo, puiss):
    mambo.fly_direct(roll=-puiss, pitch=0, yaw=0, vertical_movement=0, duration=0.1)
    
def droite(mambo, puiss):
    mambo.fly_direct(roll=puiss, pitch=0, yaw=0, vertical_movement=0, duration=0.1)

def haut(mambo, puiss):
    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=puiss, duration=0.1)
    
def bas(mambo, puiss):
    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-puiss, duration=0.1)
    
def rotation(mambo, deg):
        mambo.turn_degrees(deg)
        
def grille():
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
     
    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 20
    HEIGHT = 20
     
    # This sets the margin between each cell
    MARGIN = 5
     
    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.

    s=int(input('Dimension grille : '))


    grid = []
    for row in range(s):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(s):
            grid[row].append(0)  # Append a cell
     
    # Set row 1, cell 5 to one. (Remember rows and
    # column numbers start at zero.)
    #grid[1][5] = 1
     
    # Initialize pygame
    pygame.init()
     
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [20*s+(s+1)*5, 20*s+(s+1)*5]
    screen = pygame.display.set_mode(WINDOW_SIZE)
     
    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")
     
    # Loop until the user clicks the close button.
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    start=None
    goal=None
    mur=[] 
    manip1=None
    manip2=None
    manip3=None

    d=0
    f=0
    k=0
    l=0
    m=0
    while not done:
        for event in pygame.event.get():  # User did something
            pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if grid[row][column]==0:
                    grid[row][column] = 1
                    mur.append((column,row))
                else:
                    grid[row][column] = 0
                    mur.remove((column,row))
            elif pressed[pygame.K_d]:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if d==0:
                    grid[row][column] = 2
                    start=(column,row)
                    d=1
                elif d==1:
                    d=2
                else:
                    if grid[row][column]==2:
                        grid[row][column] = 0
                        start=None
                        d=0
            elif pressed[pygame.K_f]:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if f==0:
                    grid[row][column] = 3
                    goal=(column,row)
                    f=1
                elif f==1:
                    f=2
                else:
                    if grid[row][column]==3:
                        grid[row][column] = 0
                        goal=None
                        f=0
            elif pressed[pygame.K_k]:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if k==0:
                    grid[row][column] = 4
                    manip1=(column,row)
                    k=1
                elif k==1:
                    k=2
                else:
                    if grid[row][column]==4:
                        grid[row][column] = 0
                        manip1=None
                        k=0
            elif pressed[pygame.K_l]:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if l==0:
                    grid[row][column] = 4
                    manip2=(column,row)
                    l=1
                elif l==1:
                    l=2
                else:
                    if grid[row][column]==4:
                        grid[row][column] = 0
                        manip2=None
                        l=0
            elif pressed[pygame.K_m]:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if m==0:
                    grid[row][column] = 4
                    manip3=(column,row)
                    m=1
                elif m==1:
                    m=2
                else:
                    if grid[row][column]==4:
                        grid[row][column] = 0
                        manip3=None
                        m=0
     
        # Set the screen background
        screen.fill(BLACK)
     
        # Draw the grid
        for row in range(s):
            for column in range(s):
                color = WHITE
                if grid[row][column] == 1:
                    color = RED
                elif grid[row][column] == 2:
                    color = BLUE
                elif grid[row][column] == 3:
                    color = GREEN
                elif grid[row][column] == 4:
                    color = BLACK
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
     
        # Limit to 60 frames per second
        clock.tick(60)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
     
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

    #création graphe
    diagram = GridWithWeights(s,s)
    diagram.walls = mur

    #creation des trajets et de leurs affichages suivant le nombre de manipulations demandées
    if manip1==None:
        came_from, cost_so_far = a_star_search(diagram, start, goal)
        path=reconstruct_path(came_from, start=start, goal=goal)
        draw_grid(diagram, point_to=came_from, start=start, goal=goal)
        print()
        draw_grid(diagram, path=path)
        return path, 1
    elif manip2==None:
        came_from, cost_so_far = a_star_search(diagram, start, goal)    
        came_from1, cost_so_far1 = a_star_search(diagram, start, manip1)
        came_from2, cost_so_far2 = a_star_search(diagram, manip1, goal)
        path1=reconstruct_path(came_from1, start=start, goal=manip1)
        path2=reconstruct_path(came_from2, start=manip1, goal=goal)
        draw_grid(diagram, point_to=came_from, start=start, goal=goal)
        print()
        draw_grid(diagram, path=path1)
        print()
        draw_grid(diagram, path=path2)
        return path1, path2, 2
    elif manip3==None:
        came_from, cost_so_far = a_star_search(diagram, start, goal)    
        came_from1, cost_so_far1 = a_star_search(diagram, start, manip1)
        came_from2, cost_so_far2 = a_star_search(diagram, manip1, manip2)
        came_from3, cost_so_far3 = a_star_search(diagram, manip2, goal)
        path1=reconstruct_path(came_from1, start=start, goal=manip1)
        path2=reconstruct_path(came_from2, start=manip1, goal=manip2)
        path3=reconstruct_path(came_from3, start=manip2, goal=goal)
        draw_grid(diagram, point_to=came_from, start=start, goal=goal)
        print()
        draw_grid(diagram, path=path3)
        print()
        draw_grid(diagram, path=path2)
        print()
        draw_grid(diagram, path=path1)
        return path1, path2, path3, 3
    else:
        came_from, cost_so_far = a_star_search(diagram, start, goal)    
        came_from1, cost_so_far1 = a_star_search(diagram, start, manip1)
        came_from2, cost_so_far2 = a_star_search(diagram, manip1, manip2)
        came_from3, cost_so_far3 = a_star_search(diagram, manip2, manip3)
        came_from4, cost_so_far4 = a_star_search(diagram, manip3, goal)
        path1=reconstruct_path(came_from1, start=start, goal=manip1)
        path2=reconstruct_path(came_from2, start=manip1, goal=manip2)
        path3=reconstruct_path(came_from3, start=manip2, goal=manip3)
        path4=reconstruct_path(came_from4, start=manip3, goal=goal)
        draw_grid(diagram, point_to=came_from, start=start, goal=goal)
        print()
        draw_grid(diagram, path=path1)
        print()
        draw_grid(diagram, path=path2)
        print()
        draw_grid(diagram, path=path3)
        print()
        draw_grid(diagram, path=path4)
        return path1, path2, path3, path4, 4
    

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
def carte(path, mambo):
    #montant ou descendant
    m=1
    #avancant ou reculant
    a=1
    #meme orientation ou non
    b=0
    for i in range(len(path)-1):
        #cas meme ligne
        if path[i][0]==path[i+1][0]:
            #comparaison coordonnée colonne pour savoir rotation gauche ou droite
            if path[i][1]==path[i+1][1]+1:
                if b==0:
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==1 and c==1:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(-90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==1 and c==0:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(-90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                a=0
            else:
                if b==0:
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==1 and c==0:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==1 and c==1:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(-90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                a=1
            b=0
                
        #cas ligne différente
        else:
            #comparaison coordonnée ligne pour savoir rotation gauche ou droite            
            if path[i][0]==path[i+1][0]+1:
                if b==1:
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==0 and a==1:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(-90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==0 and a==0:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                c=1
            else:
                if b==1:
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==0 and a==0:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                elif b==0 and a==1:
                    mambo.smart_sleep(1)
                    mambo.turn_degrees(-90)
                    mambo.smart_sleep(1)
                    avant(mambo, 20)
                c=0
            b=1
            
def instruc(main):
    for i in range(len(main)):
        if main[i]==1:
            mambo.flip(direction='back')
        if main[i]==2:
            mambo.flip(direction='front')
        if main[i]==3:
            mambo.turn_degrees(180)
            mambo.turn_degrees(180)
        if main[i]==4:
            mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=20, duration=1)
            mambo.smart_sleep(1)
            mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-20, duration=1)
        if main[i]==5:
            mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=1)
            mambo.smart_sleep(1)
            mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=1)
        mambo.smart_sleep(2)
        
def anim(vic, mambo):
    if vic == 0:
        mambo.turn_degrees(40)
        mambo.smart_sleep(0.8)
        mambo.turn_degrees(-40)
    elif vic == 1:
        mambo.flip(direction='back')
    elif vic == 2:
        mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-20, duration=0.2)
        mambo.smart_sleep(2)
        mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=20, duration=0.2)
        

def vol(p, manip, mambo):
    if p[-1]==1:
        #trajet du point de départ à l'objectif
        carte(p[0], mambo)

    elif p[-1]==2:
        #trajet du point de départ au lieu de la premiere manipulation
        carte(p[0], mambo)
        mambo.smart_sleep(1)
        #realisation premiere manipulation
        instruc(manip[0])
        mambo.smart_sleep(1)
        #trajet du lieu de la premiere manipulation a l'objectif
        carte(p[1], mambo)

    elif p[-1]==3:
        #trajet du point de départ au lieu de la premiere manipulation
        carte(p[0], mambo)
        mambo.smart_sleep(1)
        #realisation premiere manipulation
        instruc(manip[0])
        mambo.smart_sleep(1)
        #trajet du lieu de la premiere manipulation au lieu de la deuxieme manipulation
        carte(p[1], mambo)
        mambo.smart_sleep(1)
        #realisation deuxieme manipulation        
        instruc(manip[1])
        mambo.smart_sleep(1)
        #trajet du lieu de la deuxieme manipulation a l'objectif       
        carte(p[2], mambo)
        
    else:
        #trajet du point de départ au lieu de la premiere manipulation
        carte(p[0], mambo)
        mambo.smart_sleep(1)
        #realisation premiere manipulation
        instruc(manip[0])
        mambo.smart_sleep(1)
        #trajet du lieu de la premiere manipulation au lieu de la deuxieme manipulation
        carte(p[1], mambo)
        mambo.smart_sleep(1)
        #realisation deuxieme manipulation        
        instruc(manip[1])
        mambo.smart_sleep(1)
        #trajet du lieu de la deuxieme manipulation au lieu de la troisieme manipulation        
        carte(p[2], mambo)
        mambo.smart_sleep(1)
        #realisation troisieme manipulation
        instruc(manip[2])
        mambo.smart_sleep(1)        
        #trajet du lieu de la troisieme manipulation a l'objectif
        carte(p[3], mambo)
        
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
        
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys


WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 800
y, y1, y3, y4 = 400, 350, 350, 300
speed = 0.5
check = False
point= 0
check_col = False
level = [10,20,30]
start = False

car_x = [0,-300,52,72] #x,y,w,h // Player car
incoming_cars = []
x_value = [-200,-120,-30,30,120,200]
#----------Algo-------------
def findZone(x1,y1,x2,y2):
   dx = x2 - x1
   dy = y2 - y1
   zone = ''
   if abs(dx) > abs(dy):
       if (dx >= 0) and (dy >= 0):
           zone = '0'
       elif (dx >= 0) and (dy <= 0):
           zone = '7'
       elif (dx <= 0) and (dy >= 0):
           zone = '3'
       else:
           zone = '4'
   else:
       if (dx >= 0) and (dy >= 0):
           zone = '1'
       elif (dx >= 0) and (dy <= 0):
           zone = '6'
       elif (dx <= 0) and (dy >= 0):
           zone = '2'
       else:
           zone = '5'
   return zone

def originalToZero(x,y,zone):
   if zone == '0':
       return x,y
   elif zone == '1':
       return y,x
   elif zone == '2':
       return -y,x
   elif zone == '3':
       return -x,y
   elif zone == '4':
       return -x,-y
   elif zone == '5':
       return -y,-x
   elif zone == '6':
       return -y,x
   else:
       return x,-y

def zeroToOriginal(x,y,zone):
   if zone == '0':
       glVertex2f(x,y)
   elif zone == '1':
       glVertex2f(y,x)
   elif zone == '2':
       glVertex2f(-y,x)
   elif zone == '3':
       glVertex2f(-x,y)
   elif zone == '4':
       glVertex2f(-x,-y)
   elif zone == '5':
       glVertex2f(-y,-x)
   elif zone == '6':
       glVertex2f(y,-x)
   else:
       glVertex2f(x,-y)

def midPoint(x1,y1,x2,y2):
   zone = findZone(x1,y1,x2,y2)
   x1,y1 = originalToZero(x1,y1,zone)
   x2,y2 = originalToZero(x2,y2,zone)
   dx = x2 - x1
   dy = y2 - y1
   d = (2*dy) - dx
   east = 2*dy
   northeast = 2*(dy-dx)
   x = x1
   y = y1
   while x <= x2:
       zeroToOriginal(x,y,zone)
       x += 1
       if d > 0:
           d += northeast
           y += 1
       else:
           d += east

def all_points(x,y,xOG,yOG):

    glVertex2f(x+xOG, y+yOG)
    glVertex2f(y+xOG, x+yOG)
    glVertex2f(y+xOG, (x*-1)+yOG)
    glVertex2f(x+xOG, (y*-1)+yOG)
    glVertex2f((x*-1)+xOG, (y*-1)+yOG)
    #glVertex2f((y*-1)+xOG,(x*-1)+yOG)
    #glVertex2f((y*-1)+xOG, x+yOG)
    glVertex2f((x*-1)+xOG, y+yOG)

def drawCircle(radius,xOG,yOG):
    d = 1 - radius
    x = 0
    y = radius
    all_points(x,y,xOG,yOG)
    while x < y:
        if d < 0:
            d = d + (2*x) + 3
            x += 1
        else:
            d = d + (2*x) - (2*y) + 5
            x += 1
            y -= 1
        all_points(x,y,xOG,yOG)
#---------ROAD-----------
def init_bar():
    global y,y1,y3,y4
    bar = []
    bar2 = []
    for i in range(9):  
        bar.append([-246, y,-246,y1])
        y-=100
        y1 -= 100
    return bar
bar = init_bar()
def init_bar2():
    global y,y1,y3,y4
    bar2 = []
    for i in range(9):  
        bar2.append([-246, y3,-246,y4])
        y3-=100
        y4 -= 100
    return bar2
bar2 = init_bar2()
def init_road():
    y= 400
    y1 = 340
    road = []
    for i in range(6):  
        road.append([None, y,None,y1])
        y-=140
        y1 -= 140
    return road
road = init_road()
#---------Draw------------
def drawRoad():
    global y, y1, y3, y4,bar,bar2
    glPointSize(5)
    glBegin(GL_POINTS)
    #--------Barrier-----------
    for i in bar:
        glColor3f(0.7,0.7,0.7)
        midPoint(i[0],i[1],i[2],i[3])
        midPoint(-i[0],i[1],-i[2],i[3])
    for i in bar2:
        glColor3f(0.9,0,0)
        midPoint(i[0],i[1],i[2],i[3])
        midPoint(-i[0],i[1],-i[2],i[3])
    #--------Road----------------
    for i in road:
        glColor3f(1,1,1)
        midPoint(82,i[1],82,i[3])
        midPoint(-82,i[1],-82,i[3])
    glEnd()
#-----------CAR----------
def drawCar(x,y):
    glColor3f(1, 1, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    midPoint(x+20,y+30,x+20,y-30)
    midPoint(x+20,y+30,x+10,y+35)
    midPoint(x+20,y-30,x+10,y-35)

    midPoint(x+20,y+15,x+25,y+15)
    midPoint(x+20,y+25,x+25,y+25)
    midPoint(x+20,y-15,x+25,y-15)
    midPoint(x+20,y-25,x+25,y-25)
    midPoint(x+25,y+15,x+25,y+25)
    midPoint(x+25,y-15,x+25,y-25)

    midPoint(x-10,y+35,x+10,y+35)
    midPoint(x-10,y-35,x+10,y-35)

    midPoint(x-20,y+30,x-20,y-30)
    midPoint(x-20,y+30,x-10,y+35)
    midPoint(x-20,y-30,x-10,y-35)

    midPoint(x-20,y+15,x-25,y+15)
    midPoint(x-20,y+25,x-25,y+25)
    midPoint(x-20,y-15,x-25,y-15)
    midPoint(x-20,y-25,x-25,y-25)
    midPoint(x-25,y+15,x-25,y+25)
    midPoint(x-25,y-15,x-25,y-25)    
    glEnd()
######--------------------------------##### Rifat  
def incdrawCar(x, y):
    glBegin(GL_POINTS)
    midPoint(x+20,y+30,x+20,y-30)
    midPoint(x+20,y+30,x+10,y+35)
    midPoint(x+20,y-30,x+10,y-35)

    midPoint(x+20,y+15,x+25,y+15)
    midPoint(x+20,y+25,x+25,y+25)
    midPoint(x+20,y-15,x+25,y-15)
    midPoint(x+20,y-25,x+25,y-25)
    midPoint(x+25,y+15,x+25,y+25)
    midPoint(x+25,y-15,x+25,y-25)

    midPoint(x-10,y+35,x+10,y+35)
    midPoint(x-10,y-35,x+10,y-35)

    midPoint(x-20,y+30,x-20,y-30)
    midPoint(x-20,y+30,x-10,y+35)
    midPoint(x-20,y-30,x-10,y-35)

    midPoint(x-20,y+15,x-25,y+15)
    midPoint(x-20,y+25,x-25,y+25)
    midPoint(x-20,y-15,x-25,y-15)
    midPoint(x-20,y-25,x-25,y-25)
    midPoint(x-25,y+15,x-25,y+25)
    midPoint(x-25,y-15,x-25,y-25)    
    glEnd()

def drawIncomingCars():
    global x_value
    for car in incoming_cars:
        glColor3f(*car[2])
        incdrawCar(car[0], car[1])

def init_incoming_cars():
    cars = []
    y_spacing = 100

    for i in range(10):
        
        x = random.choice(x_value)
        y = random.randint(300 + i * y_spacing, 1000 + i * y_spacing)

        color_choice = random.choice([(255,0,0),(255,165,0),(255,255,0),(0,0,255),(75,0,130),(128,0,128),(255,140,0),(0,128,0),(128,128,0),(0,128,128),(0,255,255),(139,0,139),(255,192,203)])
        cars.append([x, y, color_choice])
    return cars

incoming_cars = init_incoming_cars()
###############################################
def drawButton():
   
    glPointSize(3)
    glBegin(GL_POINTS)

     #---Exit----
    glColor3f(1,0,0)
    midPoint(190,380,215,350)
    midPoint(190,350,215,380)

    #----Pause----
    glColor3f(0,1,1)

    midPoint(5,380,5,350)
    midPoint(-6,350,-6,380)
    
    #Reset
    glColor3f(0.5,1,0.5)
    drawCircle(15,-200,330)
    midPoint(-210,340,-200,330)
    midPoint(-210,340,-200,350)
    glEnd()
#-----------------------
def check_collision(car1_x, car1_y, car1_width, car1_height, car2_x, car2_y, car2_width, car2_height):
    global check_col
    car1_left = car1_x - (car1_width/2)
    car1_right = car1_x + (car1_width/2)
    car1_top = car1_y + (car1_height/2)
    car1_bottom = car1_y - (car1_height/2)

    car2_left = car2_x - (car2_width/2)
    car2_right = car2_x + (car2_width/2)
    car2_top = car2_y + (car2_height/2)
    car2_bottom = car2_y - (car2_height/2)

    #collision check 
    if (car1_right >= car2_left and car1_left <= car2_right and
            car1_top >= car2_bottom and car1_bottom <= car2_top):
        check_col = True
    
def check_player_collision():
    global car_x, incoming_cars,check_col
    for car in incoming_cars:
        incoming_car_x, incoming_car_y = car[0], car[1]
        incoming_car_width = car_x[2] 
        incoming_car_height = car_x[3]
        check_collision(car_x[0], car_x[1], car_x[2], car_x[3],incoming_car_x, incoming_car_y, incoming_car_width, incoming_car_height)                          

def drawPlay():
    glBegin(GL_POINTS)
    midPoint(-60,40,60,40)
    midPoint(-60,-40,60,-40)
    midPoint(-60,-40,-60,40)
    midPoint(60,-40,60,40)
    midPoint(-15,-20,-15,20)
    midPoint(-15,-20,15,0)
    midPoint(-15,20,15,0)
    glEnd()

def show_screen():
    global check,point,check_col,start
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    ##
    drawButton()
    if start == True:
        drawRoad()
        drawCar(car_x[0], car_x[1])
        drawIncomingCars()
    ##
        score_text = f'Score: {point}'
        glColor3f(1, 1, 1)
        glRasterPos2f(-220, 355)
        for char in score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        if check and check_col != True:
            glColor3f(1, 1, 0)
            glRasterPos2f(-55, 0)
            for char in "Game Paused":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        if check_col:
            glColor3f(1, 1, 0)
            glRasterPos2f(-50, 0)
            for char in "Game Over":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

            score_text = f'Your last score: {point}'
            glRasterPos2f(-70, -30)
            for char in score_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    else:
        drawPlay()

    glutSwapBuffers()

def toggle():
    global check
    check= not check

def animate():
    global y, y1, y3, y4,bar,bar2,road,check,point,x_value,speed,start
    check_player_collision()
    if start == True:
        if check_col != True:
            if check != True:
                
            
                
                #--level try--------
                if point==level[0]:
                    speed = 0.8
                if point==level[1]:
                    speed = 1.3
                if point==level[2]:
                    speed = 1.5
                #------------------
                for i in bar:
                    i[1] -= speed
                    i[3] -= speed
                    if i[3]<-450:
                        i[1] = 450
                        i[3] = 400
                for y in bar2:
                    y[1] -= speed
                    y[3] -= speed
                    if y[3]<-450:
                        y[1] = 450
                        y[3] = 400
                for y in road:
                    y[1] -= speed
                    y[3] -= speed
                    if y[3]<-450:
                        y[1] = 450
                        y[3] = 400
                        point += 1  ## point system

                ######--------------------------------#####  Rifat    
                for car in incoming_cars:
                    car[1] -= speed
                    if car[1] < -500:
                        car[0] = random.choice(x_value)
                        car[1] = random.randint(300 , 1000)
            ######--------------------------------#####  
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global check,car_x,start
    if key==b' ':
        toggle()
    #####--------------Movement---------------##### Rifat
    if key == b'a' and not check and not check_col:
        if car_x[0] -50 > -WINDOW_WIDTH / 2:
            car_x[0] -= 15
    if key == b'd' and not check and not check_col:
        if car_x[0] + 50 < WINDOW_WIDTH / 2:
            car_x[0] += 15

    if key == b'w' and not check and not check_col:
        if car_x[1] + 50 < WINDOW_HEIGHT / 2:
            car_x[1] += 15
    if key == b's' and not check and not check_col:
        if car_x[1] - 50 > -WINDOW_HEIGHT / 2:
            car_x[1] -= 15

    if key==b'g':
        start = True

    #####--------------------------------------#####

def check_exit_button_click(x, y):
    return 435 <= x <= 470 and 750 <= y <= 785

def check_pause_button_click(x,y):
    return 240 <= x <= 260 and 750 <= y <= 785

def check_reset_button(x,y):
    return 35 <= x <= 70 and 714 <= y <= 755

def check_start_button_click(x,y):
    return 188 <= x <= 312 and 355 <= y <= 445

def mouse_click(button, state, x, y):
    global speed,check,point,check_col,incoming_cars,car_x,start
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = WINDOW_HEIGHT-y
        if check_exit_button_click(x,y):
            print('Exiting')
            glutLeaveMainLoop()

        if check_pause_button_click(x,y):
            toggle()

        if check_reset_button(x,y):
            speed = 0.5
            check = False
            point = 0
            check_col = False
            incoming_cars = init_incoming_cars()
            car_x[0] = 0
            car_x[1] =-300
            print("Resetting Game")
        
        if check_start_button_click(x,y):
            start = True
            print('starting')
            print('WASD to Move // Space = Pause')
#-----------------------

def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WINDOW_WIDTH/2, WINDOW_WIDTH/2, -WINDOW_HEIGHT/2, WINDOW_HEIGHT/2, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutMouseFunc(mouse_click)

glutInit()
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Traffic Racer")

glutDisplayFunc(show_screen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)

glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()

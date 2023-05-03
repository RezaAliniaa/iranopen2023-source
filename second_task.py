
from djitellopy import Tello
import cv2 as c
import numpy as np
import time

######################################################################
width = 640
height = 480
startCounter = 0
nesbat = 2.8
main_frame_width = width//2
main_frame_height = height//2
part_two = True
######################################################################

t = Tello()
t.connect()
t.streamon()
t.takeoff()
#time.sleep(5)

print("Battery: ", t.get_battery())

#t.rotate_clockwise(50)
t.rotate_counter_clockwise(65)
t.move_forward(75)
# First of line
while part_two:

    s=False
    left=right=False
    while(1): 
        print("Battery: ", t.get_battery())
        frame = t.get_frame_read()
        img = c.resize(frame.frame, (width, height))
        hsvFrame = c.cvtColor(img, c.COLOR_BGR2HSV) 

        pl=hsvFrame[0:720,0:50]
        ps=hsvFrame[0:720,50:600]
        pr=hsvFrame[0:720,600:720]

        plu=hsvFrame[0:100,0:720]
        prd=hsvFrame[400:500,0:720]

        sensitivity = 20
        wl = np.array([55,31,0-sensitivity], np.uint8)
        wu = np.array([86,255,255], np.uint8)  
        w_mask = c.inRange(pl, wl, wu) 
        kernal = np.ones((5, 5), "uint8") 
  
        w_mask = c.dilate(w_mask, kernal) 
        res_white = c.bitwise_and(pl, pl,mask = w_mask) 
        contours, hierarchy = c.findContours(w_mask, c.RETR_TREE, c.CHAIN_APPROX_SIMPLE) 
        for pic, contour in enumerate(contours): 
            print("left")
            t.rotate_counter_clockwise(5)
            s=True
       
        sensitivity = 20
        wl = np.array([55,31,0-sensitivity], np.uint8)
        wu = np.array([86,255,255], np.uint8)  
        w_mask = c.inRange(pr, wl, wu) 
        kernal = np.ones((5, 5), "uint8") 
  

        w_mask = c.dilate(w_mask, kernal) 
        res_white = c.bitwise_and(pr, pr, mask = w_mask) 

        contours, hierarchy = c.findContours(w_mask, c.RETR_TREE, c.CHAIN_APPROX_SIMPLE) 
        for pic, contour in enumerate(contours): 
            print ("right") 
            t.rotate_clockwise(5)
            s=True

        if(s == False):
            print("stright")
            t.move_forward(12)

        c.imshow("left",plu)
        c.imshow("right",prd)
        c.imshow("stright",ps)
        c.imshow("Multiple Color Detection in Real-TIme", img) 
        if c.waitKey(1) & 0xFF == ord('q'):
            t.move_forward(20)
            t.land()   
            c.destroyAllWindows()     
            break
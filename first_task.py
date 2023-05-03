
from djitellopy import Tello
import cv2 as c
import cv2 as cv2
import numpy as np

######################################################################
width = 640
height = 480
startCounter = 0
nesbat = 3.5
main_frame_width = width//2
main_frame_height = height//2
part_one = True
part_two = False

######################################################################

t = Tello()
t.connect()
print("Battery: ", t.get_battery())
t.streamon()
t.takeoff()
# time.sleep(5)
t.rotate_clockwise(45)
t.move_right(20)

print("Battery: ", t.get_battery())

while part_one:

    def empty(img):
        pass

    c.namedWindow("TrackBar")
    c.resizeWindow("TrackBar", 300, 300)
    c.createTrackbar("hue_min", "TrackBar", 91, 179, empty)
    c.createTrackbar("hue_max", "TrackBar", 120, 179, empty)
    c.createTrackbar("sat_min", "TrackBar", 89, 255, empty)
    c.createTrackbar("sat_max", "TrackBar", 255, 255, empty)
    c.createTrackbar("val_min", "TrackBar", 0, 255, empty)
    c.createTrackbar("val_max", "TrackBar", 255, 255, empty)

    while part_one:
        print("Battery: ", t.get_battery())
        wind = False
        go = False
        frame = t.get_frame_read()
        img = c.resize(frame.frame, (width, height))
            
        
        hsv = c.cvtColor(src=img, code=c.COLOR_BGR2HSV)
        c.circle(img, (width//2, height//2), 3, (0, 0, 255), -1)

        hue_min = c.getTrackbarPos("hue_min", "TrackBar")
        hue_max = c.getTrackbarPos("hue_max", "TrackBar")
        sat_min = c.getTrackbarPos("sat_min", "TrackBar")
        sat_max = c.getTrackbarPos("sat_max", "TrackBar")
        val_min = c.getTrackbarPos("val_min", "TrackBar")
        val_max = c.getTrackbarPos("val_max", "TrackBar")
        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])
        mask = c.inRange(hsv, lower, upper)

        cnts, hei = c.findContours(mask, c.RETR_EXTERNAL, c.CHAIN_APPROX_NONE)

        if hei is None:
            t.move_up(10)
            t.rotate_clockwise(10)
        else:
            for z in cnts:
                area = c.contourArea(z)
                print("area", area)
                if area > 1500:
                    x, y, w, h = c.boundingRect(z)
                    if w > h:
                        c.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cx = x + (w//2)
                        cy = y + (h//2)
                
                        c.circle(img, (cx, cy), 2, (0, 255, 0), -1)
                        wind = True

        if wind is False:
            t.rotate_clockwise(10)
        while wind:
            # 1
            if main_frame_width > cx:
                t.move_left(int((main_frame_width-cx)//2.6))
                # 1-1
                if main_frame_height > cy:
                    t.move_up(int((main_frame_height-cy)//nesbat))
                    go = True
                # 1-2
                if main_frame_height < cy:
                    t.move_down(int((cy-main_frame_height)//nesbat))
                    go = True
            # 2
            elif main_frame_width < cx:
                t.move_right(int((cx-main_frame_width)//2.6))
                # 2-1
                if main_frame_height > cy:
                    t.move_up(int((main_frame_height-cy)//nesbat))
                    go = True
                # 2-2
                if main_frame_height < cy:
                    t.move_down(int((cy-main_frame_width)//nesbat))
                    go = True
            else:
                t.move_back(30)

            if go:
                t.move_forward(350)
                t.rotate_counter_clockwise(180)
                t.move_forward(380)
                c.destroyAllWindows()
                part_two = True
                wind = False
                go = False
                part_one = False
    

        c.imshow("Frame", img)
        c.imshow("Mask", mask)

        if c.waitKey(1) == ord('q'):
            t.land()
            t.streamoff()
            frame.release()
            c.destroyAllWindows()
            part_one = False
            


while part_two:
    def empty(img):
        pass

    t.move_forward(20)
    t.rotate_clockwise(30)

    c.namedWindow("TrackBar")
    c.resizeWindow("TrackBar", 300, 300)
    c.createTrackbar("hue_min", "TrackBar", 0, 179, empty)
    c.createTrackbar("hue_max", "TrackBar", 21, 179, empty)
    c.createTrackbar("sat_min", "TrackBar", 71, 255, empty)
    c.createTrackbar("sat_max", "TrackBar", 255, 255, empty)
    c.createTrackbar("val_min", "TrackBar", 130, 255, empty)
    c.createTrackbar("val_max", "TrackBar", 255, 255, empty)

    while part_two:
        print("Battery: ", t.get_battery())
        wind = False
        go = False
        frame = t.get_frame_read()
        img = c.resize(frame.frame, (width, height))

        hsv = c.cvtColor(src=img, code=c.COLOR_BGR2HSV)
        c.circle(img, (width//2, height//2), 3, (0, 0, 255), -1)

        hue_min = c.getTrackbarPos("hue_min", "TrackBar")
        hue_max = c.getTrackbarPos("hue_max", "TrackBar")
        sat_min = c.getTrackbarPos("sat_min", "TrackBar")
        sat_max = c.getTrackbarPos("sat_max", "TrackBar")
        val_min = c.getTrackbarPos("val_min", "TrackBar")
        val_max = c.getTrackbarPos("val_max", "TrackBar")
        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])
        mask = c.inRange(hsv, lower, upper)

        cnts, hei = c.findContours(mask, c.RETR_EXTERNAL, c.CHAIN_APPROX_NONE)

        for z in cnts:
            area = c.contourArea(z)
            if area > 1000:
                x, y, w, h = c.boundingRect(z)
                if w > 70:
                    c.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cx = x + (w//2)
                    cy = y + (h//2)
                    c.circle(img, (cx, cy), 2, (0, 255, 0), -1)
                    wind = True
                    
        while wind:
            # 1
            if main_frame_width > cx:
                t.move_left(int((main_frame_width-cx)//2.2))
                # 1-1
                if main_frame_height > cy:
                    t.move_up(int((main_frame_height-cy)//nesbat))
                    go = True
                # 1-2
                if main_frame_height < cy:
                    t.move_down(int((cy-main_frame_height)//nesbat))
                    go = True
            # 2
            elif main_frame_width < cx:
                t.move_right(int((cx-main_frame_width)//2.2))
                # 2-1
                if main_frame_height > cy:
                    t.move_up(int((main_frame_height-cy)//nesbat))
                    go = True
                # 2-2
                if main_frame_height < cy:
                    t.move_down(int((cy-main_frame_width)//nesbat))
                    go = True

            if go:
                t.land()
                t.streamoff()
                frame.release()
                c.destroyAllWindows()
                wind = False
                go = False
                part_two = False

        c.imshow("Frame", img)
        c.imshow("hsv", hsv)
        c.imshow("Mask", mask)

        if c.waitKey(1) == ord('q'):
            t.land()
            t.streamoff()
            frame.release()
            c.destroyAllWindows()
            part_two = False
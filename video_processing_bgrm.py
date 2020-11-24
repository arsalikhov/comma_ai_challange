#!/usr/bin/env python3


import numpy as np
from cv2 import cv2
import argparse


class RemoveBG():
    
    def __init__(self):
        pass

    def play(self, video, q, k):
        font = cv2.FONT_HERSHEY_COMPLEX
        parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                                OpenCV. You can process both videos and images.')
        parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
        parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
        args = parser.parse_args()

        if args.algo == 'MOG2':
            backSub = cv2.createBackgroundSubtractorMOG2()
        else:
            backSub = cv2.createBackgroundSubtractorKNN()
        cap = cv2.VideoCapture(video)

        # Initialize frame counter
        cnt = 0

        # Some characteristics from the original video
        w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Here you can define your croping values
        x,y,h,w = 0,0,300,500

        # output
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('result.avi', fourcc, fps, (w, h))

        if (cap.isOpened()== False):  
            print("Error opening video file") 

        while(cap.isOpened()):

            ret, frame = cap.read()
            fgMask = backSub.apply(frame)

            cnt += 1
            if ret == True:
                crop_frame = frame[y:y+h, x:x+w]

                # Percentage
                xx = cnt *100/frames
                print(int(xx),'%')

                # Saving from the desired frames
                #if 15 <= cnt <= 90:
                #    out.write(crop_frame)

                # I see the answer now. Here you save all the video
                out.write(crop_frame)

                if int(cv2.__version__[0]) > 3:
                # Opencv 4.x.x
                    contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                else:
                # Opencv 3.x.x
                    _, contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
                    x = approx.ravel()[0]
                    y = approx.ravel()[1]

                    if area > 400 and area < 800:
                        cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

                        if len(approx) == 4:
                            cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
                

                cv2.imshow("video", frame)
                cv2.imshow('FG Mask', fgMask)
                cv2.imshow('croped',crop_frame)

                cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
                cv2.putText(frame, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))

        
                # press k to play next frame
                key = cv2.waitKey(0)
                while key not in [ord(q), ord(k)]:
                    key = cv2.waitKey(0)
                # Quit when 'q' is pressed
                if key == ord('q'):
                    break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

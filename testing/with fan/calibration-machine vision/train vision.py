'''
arrows: left, right, up, down: 2424832, 2555904, 2490368, 2621440
'''

import sys, os, re
import numpy as np
import cv2

tuneStuff = True

calFileDir = 'C:/Users/Nate/Documents/GitHub/arduino/shinyei-ppd42ns-arduino/testing/with fan/calibration-machine vision/calibration images/' # file with calibration images
images = []
for thing in os.listdir(calFileDir):
    if os.path.isfile(calFileDir + thing) and not re.search('thumbs',thing,re.IGNORECASE):
        images.append(thing)

samples =  np.empty((0,100))
responses = []

for imFile in images:
    print imFile
    im = cv2.imread(calFileDir + imFile)
    im = im[50:-50,0:-1]
    #im = im[100:-100, 150:-150] # for cropping file
    im3 = im.copy()

    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # for snaps from honestech tvr software
    #gaussW = 75
    #gaussH = 75
    # from dvdriver software
    gaussW = 35
    gaussH = 35
    blur = cv2.GaussianBlur(gray,(gaussW,gaussH),0)
    
    if tuneStuff:
        # choose gaussian blur amount
        while True:
            #blur = cv2.bilateralFilter(im,9,gaussW,gaussH)
            cv2.imshow('norm',blur)
            key = cv2.waitKey()
            if key == 27:
                break
            if key == 2424832: # left arrow
                if gaussW > 1:
                    gaussW -= 2
            if key == 2555904: # right arrow
                gaussW += 2
            if key == 2621440: # down arrow
                if gaussH > 1:
                    gaussH -=2
            if key == 2490368: # up arrow
                gaussH += 2
            cv2.destroyAllWindows()
            blur = cv2.GaussianBlur(gray,(gaussW,gaussH),0)
            print 'gaussH, gaussW: ', gaussH, gaussW
            
            

            
    # choose threshold block size and constant
    # 43, -4 for snaps from honestech tvr program, 33, -4 for snaps from dvdriver
    blockSize = 59
    const = -6
    cv2.destroyAllWindows()
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blockSize,const)
    if tuneStuff:
        while True:
            cv2.destroyAllWindows()
            thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blockSize,const)
            cv2.imshow('norm',thresh)
            thresh2 = thresh.copy()
            contours, hierarchy = cv2.findContours(thresh2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                [x,y,w,h] = cv2.boundingRect(cnt)
                roi = thresh2[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,0,255),2)
            key = cv2.waitKey()
            print key
            if key == 27:
                break
            if key == 2424832: # left arrow
                if blockSize > 3:
                    blockSize -= 2
            if key == 2555904: # right arrow
                blockSize += 2
            if key == 2621440: # down arrow
                const -=1
            if key == 2490368: # up arrow
                const += 1
            print 'block size:', blockSize
            print 'const: ', const

    cv2.destroyAllWindows()

    #################      Now finding Contours         ###################

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    keys = [i for i in range(48,58)]
    def getBoundRect(item):
        # returns 'x' value of bounding rectangle of contour
        return cv2.boundingRect(item)[0]
    
    srtedCntrs = sorted(contours, key = getBoundRect)
    for cnt in srtedCntrs:
        if cv2.contourArea(cnt)>100:
            [x,y,w,h] = cv2.boundingRect(cnt)

            if  h>50:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                cv2.imshow('norm',im)
                key = cv2.waitKey(0)

                if key == 27:  # (escape to quit)
                    sys.exit()
                elif key in keys:
                    responses.append(int(chr(key)))
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)
                elif key == 98: # if 'b' key is pressed, it is a square
                    continue
                    responses.append(key)
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print 'responses:', responses
print 'samples:', samples
print "training complete"

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)
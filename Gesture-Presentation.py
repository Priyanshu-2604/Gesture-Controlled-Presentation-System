import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np

# Variables
width, height = 1080, 720
folderPath = "D:/22B2492@iitb.ac.in/PythonProjects/Gesture Presentation/Presentation"

# Camera Setup
cap = cv.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

# Get the list of Presentation Images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

# Variables
imgNumber = 0
hs, ws = 120, 213 # Changing height and width of webcam output feed
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations =[[]]
annotationNumber = 0
annotationStart = False

# Hannd Detector
detector = HandDetector(detectionCon=0.8,maxHands=1)

while True:
    # Import Images
    success, img = cap.read()
    img = cv.flip(img,1 )
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        #Constrain Values for easy drawing
        xVal = int(np.interp(lmList[8][0],[500,w],[0,width]))
        yVal = int(np.interp(lmList[8][1],[100,height-200],[0,height]))
        indexFinger = xVal, yVal


        #if hand is at the height of the face
        if cy<=gestureThreshold:
            annotationStart = False
            #Gesture 1 - Left
            if fingers == [1,0,0,0,0]:
                print("Left")
                if imgNumber>0:
                    buttonPressed = True
                    annotations =[[]]
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber-=1

            #Gesture 2 - Right
            if fingers == [0,0,0,0,1]:
                print("Right")  
                if imgNumber<len(pathImages)-1:
                    buttonPressed = True
                    annotations =[[]]
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber+=1  

        #Gesture 3 - Show Pointer
        if fingers == [0,1,1,0,0]:
            cv.circle(imgCurrent, indexFinger, 12, (0,0,255),cv.FILLED)
            annotationStart = False

        #Gesture 4 - Draw
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber+=1
                annotations.append([])
            cv.circle(imgCurrent, indexFinger, 12, (0,0,255),cv.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        #Gesture 5 - Erase
        if fingers == [0,1,1,1,0]:
            if annotations:
                if annotationNumber>=0:
                    annotations.pop(-1)
                    annotationNumber-=1
                    buttonPressed = True

    else:
        annotationStart = False

    # Button Pressed Iterations
    if buttonPressed:
        buttonCounter+=1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv.line(imgCurrent,annotations[i][j-1],annotations[i][j], (0,0,200),12)


    #Adding webcam images to the SLides
    imgSmall = cv.resize(img,(ws,hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall

    cv.imshow("Slides",imgCurrent)
    cv.imshow("Image", img)
    if cv.waitKey(1)==ord('q'):
        break

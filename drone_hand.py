#Axel Velasco Chavez (Axel Meyrek) 2025
#Diego García Ricaño 2022
#Hand gestures and movement for drone control.
# Importing necessary libraries
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
from djitellopy import tello
from time import sleep
import numpy as np
import math

# Set the width and height of the video frame
w, h = 640, 480

# Flag to indicate if the drone is flying
flying = 0

# Flag to control debugging mode
debug = 0


# Function to detect hands using the webcam feed
def detectHands():
    global flying

    # Initialize the webcam
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    
    # Create a hand detector object
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    # Variables to store hand distances and hand types
    hand1dis, hand2dis = 0, 0
    handType1, handType2 = 0, 0

    # List to store finger positions
    fingers1 = [0, 0, 0, 0, 0]

    # Variables to store previous finger positions
    lx2, ly2 = 0, 0



    # Continuous loop to process video frames
    while True:
        # Read a frame from the webcam
        _, img = cap.read()

        # Find hands in the frame using the hand detector
        hands, img = detector.findHands(img)


        if hands:
            # Get the first hand in the list
            hand1 = hands[0]

            # Get hand landmarks, bounding box, center, and type
            lmList1 = hand1["lmList"]
            bbox1 = hand1["bbox"]
            centerPoint1 = hand1["center"]
            handType1 = hand1["type"]

            # Get distance between fingers
            lx1, ly1, lz1 = lmList1[0]
            lx2, ly2, lz2 = lmList1[5]
            hand1dis = np.sqrt((lx2 - lx1)**2 + (ly2 - ly1)**2)

            # Get finger positions
            fingers1 = detector.fingersUp(hand1)

        else:
            # Reset variables if no hands are detected
            midpoint = (0, 0, 0, 0, 0)
            hand1dis = 0
            hand2dis = 0
            fingers1 = [0, 0, 0, 0, 0]

        # Move the drone based on hand gestures
        moveDrone(lx2, ly2, fingers1, hand1dis)

        # Flip the image horizontally for mirror effect
        img = cv2.flip(img, 1)

        # Display the result
        cv2.imshow("Result", img)
        cv2.waitKey(1)


# Function to control the drone based on hand gestures
def moveDrone(lx2, ly2, fingers1, hand1dis):
    # Set initial values for drone movements
    ud, lr, fb, yw = 0, 0, 0, 0

    # Scaling and PID values for drone movements
    scale = 0.14
    pid = 0.6

    # Define the midpoint range for vertical movement
    midRangeX = [(h/2) - (scale * h), (h/2) + (scale * h)]

        # Get the midpoint of the hand in the X-axis
    midpointX = ly2

    # Calculate vertical movement based on the midpointX value
    if midpointX == 0 or (midpointX > midRangeX[0] and midpointX < midRangeX[1]):
        ud = 0
    elif midpointX < midRangeX[0]:
        ud = (midRangeX[0] - midpointX) * pid
    elif midpointX > midRangeX[1]:
        ud = (midRangeX[1] - midpointX) * pid

    # Clip the vertical movement value within a certain range
    ud = int(np.clip(ud, -50, 50))

    # Define the midpoint range for horizontal movement
    midRangeY = [(w/2) - (scale * w), (w/2) + (scale * w)]

    # Get the midpoint of the hand in the Y-axis
    midpointY = lx2

    # Calculate horizontal movement based on the midpointY value
    if midpointY == 0 or (midpointY > midRangeY[0] and midpointY < midRangeY[1]):
        lr = 0
    elif midpointY < midRangeY[0]:
        lr = (midRangeY[0] - midpointY) * pid
    elif midpointY > midRangeY[1]:
        lr = (midRangeY[1] - midpointY) * pid

    # Clip the horizontal movement value within a certain range
    lr = int(np.clip(lr, -50, 50))

    # Define the midpoint range for forward/backward movement
    midRangeZ = [9.5, 10.5]
    scale = 25

    # Calculate forward/backward movement based on the hand distance
    if hand1dis == 0 or (hand1dis > midRangeZ[0] and hand1dis < midRangeZ[1]):
        fb = 0
    elif hand1dis < midRangeZ[0]:
        fb = (hand1dis - midRangeZ[0]) * scale
    elif hand1dis > midRangeZ[1]:
        fb = (hand1dis - midRangeZ[1]) * scale

    # Clip the forward/backward movement value within a certain range
    fb = int(np.clip(fb, -50, 50))

    # Calculate yaw movement based on finger positions
    if fingers1 == [0, 0, 0, 0, 0]:
        yw = 0
    elif fingers1 == [1, 0, 0, 0, 0]:
        yw = -50
    elif fingers1 == [0, 1, 1, 1, 1]:
        yw = 50

    # Clip the yaw movement value within a certain range
    yw = int(np.clip(yw, -50, 50))

    # Emergency stop and land commands based on finger positions
    if fingers1 == [1, 1, 1, 0, 0]:
        me.emergency()
        print("emergency")
    if fingers1 == [0, 1, 1, 0, 1]:
        me.takeoff()
        print("take off")
    if fingers1 == [1, 1, 0, 0, 0]:
        me.land()
        print("land")

    # Print movement values and hand distance for debugging
    print(lr, fb, ud, yw)
    print(hand1dis)

	# Set the speed scale for drone movement
    speedscale = 0.6

    # Send the movement commands to the drone if not in debug mode
    if debug == 0:
        me.send_rc_control(int(lr * speedscale), int(fb * speedscale), int(ud * speedscale), yw)



# Function to start the drone and initiate hand detection
def StartDrone(me):
    global flying, debug
    
    if debug == 0:
        # Set the flying flag to indicate drone is in flying mode
        flying = 1
        # Initialize the drone's camera
        time.sleep(1)

    # Start hand detection
    detectHands()

# Main code execution starts here

# Check if not in debug mode
if debug == 0:
    # Initialize the drone object as "me"
    me = tello.Tello()
    
    # Connect to the drone, ignoring state packets
    me.connect(False)
    time.sleep(1)
    
    # Print the battery level of the drone
    print(me.get_battery())
else:
    me = 0

# Start the drone and hand detection process
StartDrone(me)

import pyautogui
import hands_module
import cv2
import time
import math

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize hand detector (update this based on the actual class implementation)
detector = hands_module.HandDetect()  # Modify this line if needed

pTime = 0

while True:
    # Read image from webcam
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    # Find hands and landmarks
    img = detector.findHands(img)
    lmlist = detector.findPos(img, draw=False)
    
    if len(lmlist):
        # Get positions of thumb, index, and middle finger tips
        x1, y1 = lmlist[4][1], lmlist[4][2]  # THUMB_TIP
        x2, y2 = lmlist[8][1], lmlist[8][2]  # INDEX_FINGER_TIP
        x3, y3 = lmlist[12][1], lmlist[12][2]  # MIDDLE_FINGER_TIP 
        
        # Calculate center point and length between index and thumb, index and middle
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length_index_thumb = math.hypot(x2 - x1, y2 - y1)
        length_index_middle = math.hypot(x3 - x2, y3 - y2)
        
        # Draw line between thumb and index finger, and between index and middle finger
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 6)
        cv2.line(img, (x2, y2), (x3, y3), (0, 255, 0), 6)
        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
        
        # Move the mouse based on center point with inverted X-axis
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width - (cx * screen_width / img.shape[1]), cy * screen_height / img.shape[0])
        
        # Perform click if hand is close
        if length_index_thumb <= 20:
            pyautogui.leftClick()

        # Perform double click if index and middle fingers are close together
        if length_index_middle <= 20:
            pyautogui.doubleClick()
        
        # Example: Swipe gesture (could be defined based on custom logic)
        # if gesture_condition_met:
        #     perform_some_action()

    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime != pTime else 0
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 4)
    
    # Display image
    cv2.imshow('WebCam', img)
    
    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()

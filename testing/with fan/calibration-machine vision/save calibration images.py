import numpy as np
import cv2

saveFileDest = 'calibration images/'
fileCounter = 0

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1) 
    if  key & 0xFF == ord('q') or key == 27:
        break
    elif key & 0xFF == ord('c'):
        cv2.imwrite(saveFileDest + str(fileCounter) + '.jpg', frame)
        fileCounter += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
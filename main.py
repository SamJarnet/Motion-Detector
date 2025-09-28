import cv2
import numpy as np


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
test, test1 = cap.read()
temp_frame = test1
while True:
    ret, frame = cap.read()
    if not np.array_equal(temp_frame, frame):
        print("motion")
    temp_frame = frame
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.imshow('Webcam Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

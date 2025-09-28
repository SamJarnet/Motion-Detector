import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Create base frames
temp_frame = None

while True:
    ret, frame_colour = cap.read()
    if not ret:
        print("Exit")
        break

    # Convert to greyscale 
    gray = cv2.cvtColor(frame_colour, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray, (11, 11), 0)
    mask_color = np.zeros_like(frame_colour)

    # Check for change
    if temp_frame is not None:
        diff = cv2.absdiff(temp_frame, blurred_frame)
        _, threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        mask_colour = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)  # convert to 3 channels or it doesnt work
        mask_colour[:, :, 0] = 0  
        mask_colour[:, :, 1] = 0 
        movement = np.any(threshold)
        print(movement)

    # Update last frame
    temp_frame = blurred_frame

    overlayed = cv2.addWeighted(frame_colour, 1.0, mask_colour, 0.5, 0)

    # Display frames
    cv2.imshow('Webcam', overlayed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

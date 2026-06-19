import cv2
import numpy as np

class MotionDetector:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.temp_frame = None
    def show_camera(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print(f"Cannot open camera {self.camera_index}")
            exit()


        while True:
            ret, frame_colour = cap.read()
            if not ret:
                print("Exit")
                break

            # Convert to greyscale 
            gray = cv2.cvtColor(frame_colour, cv2.COLOR_BGR2GRAY)
            blurred_frame = cv2.GaussianBlur(gray, (11, 11), 0)
            mask_colour = np.zeros_like(frame_colour)

            # Check for change
            if self.temp_frame is not None:
                diff = cv2.absdiff(self.temp_frame, blurred_frame)
                _, threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                mask_colour = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)  # convert to 3 channels or it doesnt work
                mask_colour[:, :, 0] = 0  
                mask_colour[:, :, 1] = 0 
                movement = np.any(threshold)
                print(movement)

            # Update last frame
            self.temp_frame = blurred_frame

            overlayed = cv2.addWeighted(cv2.convertScaleAbs(frame_colour, alpha=1.0, beta=-50), 1.0, mask_colour, 0.5, 0)

            # Display frames
            cv2.imshow('Webcam', mask_colour)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    sim = MotionDetector()
    sim.show_camera()
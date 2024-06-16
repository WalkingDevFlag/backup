import numpy as np
import cv2
import time
import mss

# Get the screen resolution
screen_width = 1920
screen_height = 1080

# Calculate the coordinates for the center pixel of the screen
center_x = screen_width // 2
center_y = screen_height // 2

# Create a monitor dictionary for the region of interest (center pixel)
monitor = {"top": center_y, "left": center_x, "width": 1, "height": 1}

with mss.mss() as sct:
    while True:
        # Capture the center pixel of the screen
        screen = np.array(sct.grab(monitor))
        
        # Get the RGB color code of the center pixel
        pixel_color = screen[0, 0]
        print("RGB Color Code of Center Pixel:", pixel_color)
        
        # Display the captured center pixel
        cv2.imshow('window', screen)
        
        # Exit loop if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

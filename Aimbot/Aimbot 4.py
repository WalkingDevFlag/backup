import numpy as np
import cv2
import time
import pygetwindow as gw
import mss


# Calculate the coordinates for the 300x300 region in the center of the game window
box_width = 300
box_height = 300
x1 = (x2 - x1 - box_width) // 2 + x1  # left
y1 = (y2 - y1 - box_height) // 2 + y1  # top

# Define the color range to track for bright red
lower_bound = np.array([140, 110, 150])
upper_bound = np.array([150, 195, 255])

# Create a monitor dictionary for the region of interest
monitor = {"top": y1, "left": x1, "width": box_width, "height": box_height}

with mss.mss() as sct:
    while True:
        # Capture the 300x300 region in the center of the game window
        screen = np.array(sct.grab(monitor))
        
        # Find the position of the colors within the specified range within the box
        red_pixels = []
        for y in range(box_height):
            for x in range(box_width):
                pixel_color = screen[y, x][:3]  # Extract BGR channels only
                if np.all(pixel_color >= lower_bound) and np.all(pixel_color <= upper_bound):
                    red_pixels.append((x, y))
        
        # Calculate the average position of red pixels
        if red_pixels:
            avg_x = sum(x for x, _ in red_pixels) // len(red_pixels)
            avg_y = sum(y for _, y in red_pixels) // len(red_pixels)
            
            # Move the mouse to the center of the cluster of red pixels
            pyautogui.moveTo(x1 + avg_x, y1 + avg_y)
        
        # Display the captured region
        cv2.imshow('window', screen)
        
        # Exit loop if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

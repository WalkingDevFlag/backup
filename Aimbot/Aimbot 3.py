import numpy as np
import cv2
import time
import pyautogui
import mss

# Get the screen resolution
screen_width, screen_height = pyautogui.size()

# Calculate the coordinates for the 200x200 region in the center of the screen
box_width = 200
box_height = 200
x1 = (screen_width - box_width) // 2  # left
y1 = (screen_height - box_height) // 2  # top
x2 = x1 + box_width  # right
y2 = y1 + box_height  # bottom

# Define the size of the 1cm x 1cm box
box_size = 10

# Define the target color (example: pure blue)
target_color = (255, 0, 0)  # BGR format

# Function to check if a pixel's RGB value matches the target color
def check_color(pixel, target_color):
    # Ensure the pixel array has correct shape and contains only RGB values
    if len(pixel) == 4:  # Ensure alpha channel is not included
        pixel = pixel[:3]
    # Compare only RGB values for equality
    return (pixel == target_color).all()

# Create a monitor dictionary for the region of interest
monitor = {"top": y1, "left": x1, "width": box_width, "height": box_height}

with mss.mss() as sct:
    while True:
        # Capture the 200x200 region in the center of the screen
        screen = np.array(sct.grab(monitor))
        
        # Convert the screen to grayscale
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        # Draw a 1cm x 1cm box in the center of the screen
        box_left = (box_width - box_size) // 2
        box_top = (box_height - box_size) // 2
        cv2.rectangle(screen, (box_left, box_top), (box_left + box_size, box_top + box_size), (0, 255, 0), 2)

        # Find the position of the target color within the box
        for y in range(box_top, box_top + box_size):
            for x in range(box_left, box_left + box_size):
                pixel_color = screen[y, x]
                if check_color(pixel_color, target_color):
                    # Move the mouse to the center of the detected color
                    pyautogui.moveTo(x1 + x, y1 + y)
                    break
        
        # Display the captured region with the box drawn
        cv2.imshow('window', screen)
        
        # Exit loop if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

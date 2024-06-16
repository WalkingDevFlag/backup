import cv2
import numpy as np
import operator
import tensorflow as tf
import pyautogui
import time
import webbrowser

# Digit Recognizer Model
new_model = tf.keras.models.load_model('E:\\Sid Folder\\Random Python Scripts\\Sudoku-Solver-CNN-OCR\\ocr_v2.h5')

# To order predicted digit nested list
def display_predList(predList):
    predicted_digits = []
    for i in range(len(predList)):
        for j in range(len(predList)):
            predicted_digits.append(predList[j][i])
    return predicted_digits

# Parameters for Warping the image
margin = 10
case = 28 + 2 * margin
perspective_size = 9 * case

# Function to solve Sudoku using backtracking
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0

    return False

def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

# Take a screenshot from the website
webbrowser.open_new("https://sudoku.com/extreme/")
time.sleep(5)
screenshot_path = "E:\\Sid Folder\\Random Python Scripts\\Sudoku-Solver-CNN-OCR\\Web Screenshots\\sudoku_screenshot.png"
pyautogui.screenshot(screenshot_path)
print("Screenshot saved successfully")

# Load the screenshot instead of capturing from the webcam
frame = cv2.imread(screenshot_path)
p_frame = frame.copy()

# Process the frame to find contour
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)

# Get all the contours in the frame
contours_, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour = None
maxArea = 0

# Find the largest contour (Sudoku Grid)
for c in contours_:
    area = cv2.contourArea(c)
    if area > 25000:
        peri = cv2.arcLength(c, True)
        polygon = cv2.approxPolyDP(c, 0.01 * peri, True)
        if area > maxArea and len(polygon) == 4:
            contour = polygon
            maxArea = area

# Draw the contour and extract Sudoku Grid
if contour is not None:
    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
    points = np.vstack(contour).squeeze()
    points = sorted(points, key=operator.itemgetter(1))

    if points[0][0] < points[1][0]:
        if points[3][0] < points[2][0]:
            pts1 = np.float32([points[0], points[1], points[3], points[2]])
        else:
            pts1 = np.float32([points[0], points[1], points[2], points[3]])
    else:
        if points[3][0] < points[2][0]:
            pts1 = np.float32([points[1], points[0], points[3], points[2]])
        else:
            pts1 = np.float32([points[1], points[0], points[2], points[3]])

    pts2 = np.float32([[0, 0], [perspective_size, 0], [0, perspective_size], [perspective_size, perspective_size]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspective_window = cv2.warpPerspective(p_frame, matrix, (perspective_size, perspective_size))
    result = perspective_window.copy()

    # Process the extracted Sudoku Grid
    p_window = cv2.cvtColor(perspective_window, cv2.COLOR_BGR2GRAY)
    p_window = cv2.GaussianBlur(p_window, (5, 5), 0)
    p_window = cv2.adaptiveThreshold(p_window, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    p_window = cv2.morphologyEx(p_window, cv2.MORPH_CLOSE, vertical_kernel)
    lines = cv2.HoughLinesP(p_window, 1, np.pi / 180, 120, minLineLength=40, maxLineGap=10)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(perspective_window, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Invert the grid for digit recognition
    invert = 255 - p_window
    invert_window = invert.copy()
    invert_window = invert_window / 255

    i = 0
    flag = 0
    ans = 0
    if flag != 1:
        predicted_digits = []
        pixels_sum = []

    # To get individual cells
    for y in range(9):
        predicted_line = []
        for x in range(9):
            y2min = y * case + margin
            y2max = (y + 1) * case - margin
            x2min = x * case + margin
            x2max = (x + 1) * case - margin

            # Obtained Cell
            image = invert_window[y2min:y2max, x2min:x2max]

            # Process the cell to feed it into the model
            img = cv2.resize(image, (28, 28))
            img = img.reshape((1, 28, 28, 1))

            # Get sum of all the pixels in the cell
            pixel_sum = np.sum(img)
            pixels_sum.append(pixel_sum)

            # Predict the digit in the cell
            pred = new_model.predict(img)
            predicted_digit = pred.argmax()

            # For blank cells set predicted digit to 0
            if pixel_sum > 775.0:
                predicted_digit = 0

            predicted_line.append(predicted_digit)

            i = i + 1

        # Get predicted digit list
        if flag != 1:
            predicted_digits.append(predicted_line)

    # Get solved Sudoku
    ans = solve(predicted_digits)
    if ans == True:
        flag = 1
        pred_digits = display_predList(predicted_digits)

        # Print the solved Sudoku as a 2D array
        print("Solved Sudoku:")
        for row in predicted_digits:
            print(row)
else:
    print("Sudoku grid not found.")

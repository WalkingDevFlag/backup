import webbrowser
import pyautogui
import time

webbrowser.open_new("https://sudoku.com/extreme/")
time.sleep(5)

pyautogui.screenshot("E:\\Sid Folder\\Random Python Scripts\\Sudoku-Solver-CNN-OCR\\Web Screenshots\\sudoku_screenshot.png") #Screenshot Path

print("Screenshot saved successfully")

import pyautogui
import time

while True:
    x, y = pyautogui.position()
    print(f"Tọa độ chuột: ({x}, {y})")
    time.sleep(1)
import pyautogui
import keyboard
import threading
import time

# Vị trí cần click
click_position = (2309, 1579)

# Biến điều khiển trạng thái click
clicking = False

def auto_click():
    global clicking
    while True:
        if clicking:
            pyautogui.click(click_position)
            time.sleep(0.01)  # thời gian giữa các lần click (giảm để click nhanh hơn)
        else:
            time.sleep(0.01)

def toggle_click():
    global clicking
    clicking = not clicking
    print("Clicking:", "Bắt đầu" if clicking else "Dừng")

# Tạo luồng click riêng biệt
click_thread = threading.Thread(target=auto_click)
click_thread.daemon = True
click_thread.start()

# Lắng nghe phím 's'
keyboard.add_hotkey('s', toggle_click)

print("Nhấn 's' để bắt đầu/dừng click. Nhấn 'esc' để thoát.")
keyboard.wait('esc')
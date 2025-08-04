import pyautogui
import time

def test_scroll_chuot(cuon_chuot_y=-180, delay_click=0.2, delay_scroll=1.0):
    toa_do_click = (2535, 1392)

    print(f"🖱️ Di chuyển và click tại {toa_do_click}...")
    pyautogui.moveTo(*toa_do_click, duration=delay_click)
    pyautogui.click()

    print(f"⏳ Chờ {delay_scroll} giây trước khi cuộn chuột...")
    time.sleep(delay_scroll)

    pyautogui.scroll(cuon_chuot_y)
    print(f"✅ Đã scroll xuống {abs(cuon_chuot_y)} pixel")

time.sleep(3)

test_scroll_chuot()  # Cuộn mặc định -200px

time.sleep(1)
pyautogui.scroll(-180)

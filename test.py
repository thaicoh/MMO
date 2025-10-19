import pyautogui
import cv2
import numpy as np

def chup_va_so_sanh_da_chon_tat_ca_chua(anh_mau, nguong_giong=0.95):
    """
    Chụp vùng màn hình rồi so sánh với ảnh mẫu.
    Trả về True nếu giống, False nếu khác.
    
    Parameters:
    - anh_mau (str): đường dẫn đến ảnh mẫu để so sánh
    - nguong_giong (float): mức độ giống nhau (0.0–1.0), mặc định 0.95
    """
    # Tọa độ góc trên trái và góc dưới phải
    x1, y1 = 1936, 1541
    x2, y2 = 1983, 1596
    width, height = x2 - x1, y2 - y1

    # Chụp vùng màn hình
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Đọc ảnh mẫu
    template = cv2.imread(anh_mau)
    if template is None:
        print(f"❌ Không tìm thấy ảnh mẫu: {anh_mau}")
        return False

    # Resize ảnh mẫu để so sánh cùng kích thước
    template = cv2.resize(template, (width, height))

    # So sánh bằng phương pháp hệ số tương quan
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    similarity = cv2.minMaxLoc(result)[1]  # lấy giá trị max similarity

    print(f"🔍 Độ giống nhau: {similarity:.4f}")

    if similarity >= nguong_giong:
        print("✅ Ảnh chụp giống ảnh mẫu.")
        return True
    else:
        print("❌ Ảnh chụp KHÔNG giống ảnh mẫu.")
        return False

if chup_va_so_sanh_da_chon_tat_ca_chua(r"C:\Users\84765\Desktop\AutoClick\mauOCLickChonTatCa.png"):
    print("Hai ảnh giống nhau!")
else:
    print("Hai ảnh khác nhau!")

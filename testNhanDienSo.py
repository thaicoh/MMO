import pytesseract
import cv2
import numpy as np
from PIL import Image

# Chỉ định đường dẫn tới tesseract nếu cần (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def nhan_dien_so_tu_anh(duong_dan_anh):
    try:
        # 1. Đọc ảnh
        img = cv2.imread(duong_dan_anh)

        # 2. Cắt 1% mép trái/phải
        h, w = img.shape[:2]
        left = int(w * 0.01)
        right = int(w * 0.99)
        img = img[:, left:right]

        # 3. Thêm padding trắng
        padding = 50
        img = cv2.copyMakeBorder(
            img, padding, padding, padding, padding,
            cv2.BORDER_CONSTANT, value=[255, 255, 255]
        )

        # 4. Chuyển sang xám
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 5. Nhị phân hóa
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

        # 6. Loại đốm nhỏ
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) < 30:
                cv2.drawContours(thresh, [cnt], -1, 0, -1)

        # 7. Làm đầy số
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        # 8. Đảo màu
        inverted = cv2.bitwise_not(closed)

        # 9. Phóng to ảnh
        scale_up = cv2.resize(inverted, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

        # 10. Lưu ảnh sau xử lý (tuỳ chọn)
        cv2.imwrite("processed.png", scale_up)

        # 11. OCR lần 1 với psm 8
        config1 = '--psm 8 -c tessedit_char_whitelist=0123456789'
        text1 = pytesseract.image_to_string(scale_up, config=config1)
        so1 = ''.join(filter(str.isdigit, text1))

        if so1:
            print(f"[OCR Lần 1 - psm8]: '{text1.strip()}' ➤ Kết quả: {so1}")
            return so1

        # 12. OCR lần 2 với psm 7 nếu không nhận được kết quả ở lần 1
        config2 = '--psm 6 -c tessedit_char_whitelist=0123456789'
        text2 = pytesseract.image_to_string(scale_up, config=config2)
        so2 = ''.join(filter(str.isdigit, text2))

        print(f"[OCR Lần 2 - psm7]: '{text2.strip()}' ➤ Kết quả: {so2}")
        return so2

    except Exception as e:
        print(f"❌ Lỗi OCR: {e}")
        return None

# Ví dụ gọi hàm
print("Kết quả:", nhan_dien_so_tu_anh("anhSoCuaVideo.png"))

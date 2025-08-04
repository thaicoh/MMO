import pyautogui
import time
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Chỉ định đường dẫn đến tesseract.exe nếu cần
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

moTaVideo = "#ShopeeCreator #ShopeeStyle #ShopeeVideo #LuotVuiMuaLien #VideohangDoiSong #VideohangTieuDung #VideohangGiaDung Xịn lắmm 😻"
linkSP = ""

def click_nut_dang_video(vitri_nut=(2540, 1637), delay=0.5, timeout=2, threshold=0.95):
    # Xác định vùng ảnh quanh nút
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("truoc_click.png", region=vung_nut)
    
    print(f"Đang click tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click, chờ giao diện phản hồi...")

    time.sleep(timeout)  # chờ phản hồi giao diện

    # Chụp lại ảnh sau khi click
    pyautogui.screenshot("sau_click.png", region=vung_nut)

    # So sánh ảnh trước & sau để kiểm tra nút còn không
    img1 = cv2.imread("truoc_click.png")
    img2 = cv2.imread("sau_click.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng giữa trước & sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Nút đã biến mất hoặc thay đổi → Click THÀNH CÔNG.")
        return True
    else:
        print("⚠️ Nút vẫn còn → Click có thể KHÔNG thành công.")
        return False
    
def click_nut_thu_vien(vitri_nut=(2535, 1392), delay=0.5, timeout=1, threshold=0.95):
    # 📸 Vùng chụp ảnh để so sánh toàn bộ giao diện (giống như hàm ảnh bìa)
    vung_so_sanh = (1911, 117, 2686 - 1911, 1687 - 117)

    # Vùng nút giữ nguyên
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("thu_vien_truoc.png", region=vung_so_sanh)

    print(f"Click nút Thư viện tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp lại sau khi click
    pyautogui.screenshot("thu_vien_sau.png", region=vung_so_sanh)

    img1 = cv2.imread("thu_vien_truoc.png")
    img2 = cv2.imread("thu_vien_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Thư viện thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def click_chon_video(delay=0.5, timeout=3, threshold=0.95):
    global vitri_chon_video, so_lan_click_video, cuon_chuot_y
    time.sleep(1)

    # Lần đầu cố định vị trí nút
    if so_lan_click_video == 0:
        vitri_nut = (2001, 415)
    else:
        vitri_nut = tuple(vitri_chon_video)

    # Vùng để xác định nút (vẫn giữ nguyên)
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # 📸 Vùng chụp ảnh mở rộng để so sánh
    vung_so_sanh = (1911, 117, 2686 - 1911, 1687 - 117)

    pyautogui.screenshot("video_truoc.png", region=vung_so_sanh)
    print(f"Click chọn video tại {vitri_nut} (lần thứ {so_lan_click_video + 1}) sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    pyautogui.screenshot("video_sau.png", region=vung_so_sanh)
    img1 = cv2.imread("video_truoc.png")
    img2 = cv2.imread("video_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click chọn video thành công.")

        # Cập nhật vị trí cho lần kế tiếp
        so_lan_click_video += 1

        if so_lan_click_video == 1:
            vitri_chon_video = [2201, 415]
        elif so_lan_click_video % 4 != 0:
            vitri_chon_video[0] += 200
        else:
            vitri_chon_video = [2001, 415]
            cuon_chuot_y += 180

        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def click_nut_tiep_theo(vitri_nut=(2555, 1605), delay=0.5, timeout=2, threshold=0.95):
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("tiep_theo_truoc.png", region=vung_nut)

    print(f"Click nút Tiếp theo tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp lại sau khi click
    pyautogui.screenshot("tiep_theo_sau.png", region=vung_nut)

    img1 = cv2.imread("tiep_theo_truoc.png")
    img2 = cv2.imread("tiep_theo_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Tiếp theo thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

import pyautogui
import cv2
import time

def click_nut_chon_anh_bia(vitri_nut=(2041, 510), delay=0.5, timeout=2, threshold=0.95):
    # 📸 Vùng so sánh ảnh cố định
    vung_so_sanh = (1911, 117, 2686 - 1911, 1687 - 117)

    # Vùng nút (vẫn mở rộng như cũ)
    width = 250
    height = 150
    vung_nut = (
        vitri_nut[0] - width // 2,
        vitri_nut[1] - height // 2,
        width,
        height
    )

    # Chụp ảnh trước khi click
    pyautogui.screenshot("anh_bia_truoc.png", region=vung_so_sanh)

    print(f"Click nút chọn ảnh bìa tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp ảnh sau khi click
    pyautogui.screenshot("anh_bia_sau.png", region=vung_so_sanh)

    # So sánh ảnh
    img1 = cv2.imread("anh_bia_truoc.png")
    img2 = cv2.imread("anh_bia_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click chọn ảnh bìa thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def chup_anh_so_video(filename="anhSoCuaVideo.png"):
    # Tọa độ góc trên bên trái
    x1, y1 = 2231, 766
    # Tọa độ góc dưới bên phải (ví dụ)
    x2, y2 = 2369, 880

    width = x2 - x1
    height = y2 - y1

    # Chụp ảnh vùng xác định
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot.save(filename)
    print(f"✅ Đã lưu ảnh vào: {filename}")

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

def click_thoat_chon_anh_bia(vitri_nut=(1972, 173), delay=0.5, timeout=1, threshold=0.95):
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("thoat_bia_truoc.png", region=vung_nut)

    print(f"Click nút Thoát ảnh bìa tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp lại sau khi click
    pyautogui.screenshot("thoat_bia_sau.png", region=vung_nut)

    img1 = cv2.imread("thoat_bia_truoc.png")
    img2 = cv2.imread("thoat_bia_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Thoát ảnh bìa thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def click_nut_nhan_them_san_pham(vitri_nut=(2319, 624), delay=0.5, timeout=1, threshold=0.95):
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("them_san_pham_truoc.png", region=vung_nut)

    print(f"Click nút Nhận thêm sản phẩm tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp lại sau khi click
    pyautogui.screenshot("them_san_pham_sau.png", region=vung_nut)

    img1 = cv2.imread("them_san_pham_truoc.png")
    img2 = cv2.imread("them_san_pham_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Nhận thêm sản phẩm thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def click_nut_them_lien_ket(vitri_nut=(2633, 157), delay=2, timeout=2, threshold=0.97):
    # Vùng nút giữ nguyên
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # 📸 Vùng chụp ảnh rộng để so sánh trước/sau
    vung_so_sanh = (1911, 117, 2686 - 1911, 1687 - 117)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("them_lien_ket_truoc.png", region=vung_so_sanh)
    time.sleep(delay)
    print(f"Click nút Thêm liên kết tại {vitri_nut} sau {delay} giây...")
    
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp ảnh sau khi click
    pyautogui.screenshot("them_lien_ket_sau.png", region=vung_so_sanh)

    img1 = cv2.imread("them_lien_ket_truoc.png")
    img2 = cv2.imread("them_lien_ket_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Thêm liên kết thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

import pyautogui
import pyperclip
import time

def click_va_dan_link(vitri_o=(1994, 364), doan_text=""):
    print(f"Click tại {vitri_o} và dán link...")
    pyperclip.copy(doan_text)          # Copy vào clipboard
    pyautogui.moveTo(*vitri_o, duration=0.2)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")      # Dán từ clipboard
    print("✅ Đã dán link thành công.")

def click_nut_nhap(vitri_nut=(2257, 730), delay=0.5, timeout=1, threshold=0.95):
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("nhap_truoc.png", region=vung_nut)

    print(f"Click nút Nhập tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp lại sau khi click
    pyautogui.screenshot("nhap_sau.png", region=vung_nut)

    img1 = cv2.imread("nhap_truoc.png")
    img2 = cv2.imread("nhap_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Nhập thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def click_nut_chon_tat_ca_san_pham(delay=0.5, timeout=1, threshold=0.95):
    time.sleep(1)
    
    toa_do_1 = (1957, 1573)
    toa_do_2 = (2464, 1591)
    vung_nut_2 = (toa_do_2[0] - 50, toa_do_2[1] - 30, 100, 60)

    # Click lần 1 (không kiểm tra)
    print(f"Click lần 1 tại {toa_do_1}")
    pyautogui.moveTo(*toa_do_1, duration=0.2)
    pyautogui.click()
    time.sleep(1)

    # Chụp ảnh trước khi click lần 2
    pyautogui.screenshot("chon_tat_ca_truoc.png", region=vung_nut_2)

    # Click lần 2
    print(f"Click lần 2 tại {toa_do_2} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*toa_do_2, duration=0.2)
    pyautogui.click()
    print("Đã click lần 2. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp ảnh sau khi click lần 2
    pyautogui.screenshot("chon_tat_ca_sau.png", region=vung_nut_2)

    img1 = cv2.imread("chon_tat_ca_truoc.png")
    img2 = cv2.imread("chon_tat_ca_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Chọn tất cả sản phẩm thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def click_va_dan_mo_ta_video(vitri_o=(2235, 294), doan_text=""):
    print(f"Click tại {vitri_o} và them mo ta...")
    pyperclip.copy(doan_text)          # Copy vào clipboard
    pyautogui.moveTo(*vitri_o, duration=0.2)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")      # Dán từ clipboard
    print("✅ Đã dán link thành công.")

def click_nut_dong_y_mo_ta(vitri_nut=(2609, 174), delay=0.5, timeout=1, threshold=0.95):
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("dong_y_mo_ta_truoc.png", region=vung_nut)

    print(f"Click nút Đồng ý nhập mô tả tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp lại sau khi click
    pyautogui.screenshot("dong_y_mo_ta_sau.png", region=vung_nut)

    img1 = cv2.imread("dong_y_mo_ta_truoc.png")
    img2 = cv2.imread("dong_y_mo_ta_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Đồng ý nhập mô tả thành công.")
        return True
    else:
        print("⚠️ Nút vẫn còn, có thể chưa phản hồi.")
        return False

def click_chon_anh_bia_moi(delay1=0.5, delay2=0.5, timeout=1, threshold=0.95):
    toa_do_1 = (2015, 1487)
    toa_do_2 = (2628, 178)
    vung_nut_2 = (toa_do_2[0] - 50, toa_do_2[1] - 30, 100, 60)

    # Click lần 1 (không kiểm tra)
    print(f"Click lần 1 tại {toa_do_1}")
    time.sleep(delay1)
    pyautogui.moveTo(*toa_do_1, duration=0.2)
    pyautogui.click()

    # Chụp ảnh trước khi click lần 2
    pyautogui.screenshot("anh_bia_moi_truoc.png", region=vung_nut_2)

    # Click lần 2 (có kiểm tra)
    print(f"Click lần 2 tại {toa_do_2}")
    time.sleep(delay2)
    pyautogui.moveTo(*toa_do_2, duration=0.2)
    pyautogui.click()
    print("Đã click lần 2. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp ảnh sau khi click
    pyautogui.screenshot("anh_bia_moi_sau.png", region=vung_nut_2)

    img1 = cv2.imread("anh_bia_moi_truoc.png")
    img2 = cv2.imread("anh_bia_moi_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click chọn ảnh bìa mới thành công.")
        return True
    else:
        print("⚠️ Giao diện chưa thay đổi rõ ràng.")
        return False

def click_nut_dang(vitri_nut=(2357, 1625), delay=0.5, timeout=2, threshold=0.95):
    
    

    time.sleep(1.5)
    
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("dang_truoc.png", region=vung_nut)

    print(f"Click nút Đăng tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click. Chờ phản hồi...")

    time.sleep(timeout)

    # Chụp lại sau khi click
    pyautogui.screenshot("dang_sau.png", region=vung_nut)

    img1 = cv2.imread("dang_truoc.png")
    img2 = cv2.imread("dang_sau.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh_img)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng ảnh trước/sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Click nút Đăng thành công.")
        return True
    else:
        print("⚠️ Giao diện chưa thay đổi rõ ràng.")
        return False

def click_tro_ve_home(vitri_nut=(1962, 155), delay=0.5):
    print(f"Click nút Trở về Home tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("✅ Đã click nút Trở về Home.")

def thu_lai_click(func, so_lan_thu=2, delay=1):
    for lan in range(so_lan_thu):
        if func():
            return True
        print(f"⚠️ Click thất bại lần {lan + 1}, thử lại...")
        time.sleep(delay)
    print("❌ Đã thử nhiều lần nhưng vẫn thất bại.")
    return False

def click_nut_ban_nhap(vitri_nut=(1986, 1624), delay=0.5, timeout=2, threshold=0.95):
    # Xác định vùng ảnh quanh nút
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)

    # Chụp ảnh trước khi click
    pyautogui.screenshot("truoc_click_bannhap.png", region=vung_nut)

    print(f"Đang click nút Bản nháp tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("Đã click, chờ giao diện phản hồi...")

    time.sleep(timeout)  # Chờ giao diện phản hồi

    # Chụp lại ảnh sau khi click
    pyautogui.screenshot("sau_click_bannhap.png", region=vung_nut)

    # So sánh ảnh trước & sau để kiểm tra nút có thay đổi
    img1 = cv2.imread("truoc_click_bannhap.png")
    img2 = cv2.imread("sau_click_bannhap.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"Độ tương đồng trước & sau khi click: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Nút đã biến mất hoặc thay đổi → Click THÀNH CÔNG.")
        return True
    else:
        print("⚠️ Nút vẫn còn → Click có thể KHÔNG thành công.")
        return False

def click_nut_back(vitri_nut=(1957, 165), delay=0.5, timeout=2, threshold=0.95):
    # 📸 Vùng so sánh ảnh cố định (không phải vùng quanh nút)
    vung_so_sanh = (1911, 117, 2686 - 1911, 1687 - 117)

    # Chụp ảnh giao diện trước khi click
    pyautogui.screenshot("giao_dien_truoc_click_back.png", region=vung_so_sanh)

    print(f"🔙 Đang click nút Back tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print("⏳ Đã click, chờ phản hồi giao diện...")

    time.sleep(timeout)  # Chờ giao diện phản hồi

    # Chụp lại ảnh giao diện sau khi click
    pyautogui.screenshot("giao_dien_sau_click_back.png", region=vung_so_sanh)

    # So sánh sự thay đổi của giao diện
    img1 = cv2.imread("giao_dien_truoc_click_back.png")
    img2 = cv2.imread("giao_dien_sau_click_back.png")

    if img1 is None or img2 is None:
        print("❌ Không đọc được ảnh so sánh.")
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)

    print(f"📊 Độ tương đồng giao diện trước & sau: {similarity:.2f}")

    if similarity < threshold:
        print("✅ Giao diện đã thay đổi → Click Back THÀNH CÔNG.")
        return True
    else:
        print("⚠️ Giao diện không đổi nhiều → Có thể KHÔNG thành công.")
        return False

def dang_1_video():

    time.sleep(2)

    soKhongCoTrongData = False
    
    result = click_nut_dang_video()

    if not result:
        print("❌ Không thể bắt đầu đăng video.")
        return False

    if not click_nut_thu_vien():
        return False
    
    # 💡 Scroll nếu đang xử lý video từ lần thứ 5 trở đi
    if so_lan_click_video >= 4:
        pyautogui.scroll(-cuon_chuot_y)
        print(f"🖱️ Đã scroll xuống {cuon_chuot_y} pixel")

    if not click_chon_video():
        return False

    if not click_nut_tiep_theo():
        return False

    if not click_nut_tiep_theo():
        return False

    if not thu_lai_click(click_nut_chon_anh_bia):
        return False

    time.sleep(1)
    chup_anh_so_video()
    time.sleep(0.2)

    so = nhan_dien_so_tu_anh("anhSoCuaVideo.png")
    if not so:
        print("❌ Không nhận diện được số.")
        return False
    else:
        print(f"📌 Đã nhận diện được số: {so}")

        # ✅ Dán link tương ứng nếu số có trong data
        try:
            so_int = int(so)
            if so_int in data:
                link_tuong_ung = data[so_int]
                print(f"🔗 Dán link tương ứng từ file Excel: {link_tuong_ung}")
            else:
                # Xu ly click luu ban nhap 
                soKhongCoTrongData = True

        except:
            print("⚠️ Không thể chuyển số sang int, dùng linkSP mặc định.")
            click_va_dan_link(doan_text="linkSP")



    videoDangO = so


    if not click_thoat_chon_anh_bia():
        return False
    
    if soKhongCoTrongData == True:

        if click_nut_ban_nhap():
            print("✅ Da Huy Dang Video vi khong co link trong data.")
            time.sleep(1)
            click_tro_ve_home()

            with open(pathLog, "a", encoding="utf-8") as f:
            
                f.write(f"{videoDangO} Khong Thanh Cong: Khong co link trong data\n")
            
            return True
        
    else:

        if not click_nut_nhan_them_san_pham():
            return False

        if not click_nut_them_lien_ket():
            return False


        # ✅ Dán link tương ứng nếu số có trong data
        try:
            so_int = int(so)
            if so_int in data:
                link_tuong_ung = data[so_int]
                print(f"🔗 Dán link tương ứng từ file Excel: {link_tuong_ung}")
                click_va_dan_link(doan_text=link_tuong_ung)
            else:
                print("⚠️ Không tìm thấy số trong file, dùng linkSP mặc định.")
                click_va_dan_link(doan_text=linkSP)
        except:
            print("⚠️ Không thể chuyển số sang int, dùng linkSP mặc định.")
            click_va_dan_link(doan_text="linkSP")

        if not click_nut_nhap():
            return False

        time.sleep(1)

        if not click_nut_chon_tat_ca_san_pham():

            if not click_nut_back():
                return False
            if not click_nut_back():
                return False
            
            if click_nut_ban_nhap():
                print("✅ Da Huy Dang Video vi link khong co san pham.")
                time.sleep(1)
                click_tro_ve_home()

                with open(pathLog, "a", encoding="utf-8") as f:
                
                    f.write(f"{videoDangO} Khong Thanh Cong: khong tim thay san pham tu link\n")
                
                return True
            
            return False


        time.sleep(1)

        click_va_dan_mo_ta_video(doan_text=moTaVideo)

        time.sleep(0.1)

        if not click_nut_dong_y_mo_ta():
            return False

        if not click_nut_chon_anh_bia():
            return False

        if not click_chon_anh_bia_moi():
            return False

        time.sleep(0.5)

        if click_nut_dang():
            print("✅ Video đã được đăng.")
            time.sleep(1)
            click_tro_ve_home()

            with open(pathLog, "a", encoding="utf-8") as f:
            
                f.write(f"{videoDangO} thanh cong\n")
            
            return True
        else:
            
            if click_nut_dang():
                print("✅ Video đã được đăng.")
                time.sleep(1)
                click_tro_ve_home()

                with open(pathLog, "a", encoding="utf-8") as f:
                
                    f.write(f"{videoDangO} thanh cong\n")
                
                return True
        
            print("❌ Đăng video thất bại.")

            with open("log.txt", "a", encoding="utf-8") as f:
            
            
                f.write(f"{videoDangO} loi\n")
                print("⛔ Dừng chương trình do lỗi trong quá trình đăng.")

            return False
        


import pandas as pd
import re

def doc_file_va_tra_ve_dict_so_link(duong_dan_file: str, ten_sheet: str = "Sheet1") -> dict:
    """
    Đọc file Excel và trả về dict có dạng {số: link_tương_ứng}
    """
    try:
        df = pd.read_excel(duong_dan_file, sheet_name=ten_sheet)
        noi_dung = df.iloc[:, 0].tolist()  # lấy cột đầu tiên (thường là 'Nội dung')

        ket_qua = {}
        i = 0
        while i < len(noi_dung) - 1:
            dong = str(noi_dung[i])
            match = re.match(r"(\d+)\.", dong)
            if match:
                so = int(match.group(1))
                link = str(noi_dung[i + 1]).strip()
                if link and link.lower() != "nan":
                    ket_qua[so] = link
                i += 3  # bỏ qua dòng trống
            else:
                i += 1
        return ket_qua

    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")
        return {}

data = doc_file_va_tra_ve_dict_so_link(r"C:\Users\84765\Downloads\DA5_output_final_14.xlsx")
pathLog = r"C:\Users\84765\Desktop\AutoClick\Log\Acc2\log_20.7.txt"

# In kết quả
for so, link in data.items():
    print(f"{so} ➤ {link}")

# Biến toàn cục để chọn video mới sau mỗi lần đăng
vitri_chon_video = [2535, 1392]
so_lan_click_video = 0
cuon_chuot_y = 0

time.sleep(3)

videoDangO = 10000

so_video_muon_dang = 40  # số video muốn đăng

for i in range(so_video_muon_dang):
    print(f"\n========================")
    print(f"🎬 BẮT ĐẦU ĐĂNG VIDEO THỨ {i+1}")
    print(f"========================")
    if not dang_1_video():
        print("⛔ Dừng chương trình do lỗi trong quá trình đăng.")
        break

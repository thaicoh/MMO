import pyautogui
import time
import cv2
import numpy as np
import pytesseract
from PIL import Image
import pyautogui
import pyperclip
import time
import pyautogui
import cv2
import time
import pandas as pd
import re
import random

# Chỉ định đường dẫn đến tesseract.exe nếu cần
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import numpy as np
import cv2

def imread_unicode(path):
    """Đọc ảnh có tên Unicode (có dấu tiếng Việt)."""
    try:
        data = np.fromfile(path, dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"⚠️ Lỗi đọc ảnh '{path}': {e}")
        return None



# Tọa độ các nút cho các hàm
nutDangVideo = (2540, 1637)  # click_nut_dang_video
nutThuVien = (2535, 1392)    # click_nut_thu_vien
nutChonVideo = (2001, 415)   # click_chon_video (tọa độ lần đầu)
nutTiepTheo = (2555, 1605)   # click_nut_tiep_theo
nutChonAnhBia = (2041, 510)  # click_nut_chon_anh_bia
nutSoVideo = (2231, 766)     # chup_anh_so_video (góc trên bên trái)
nutThoatChonAnhBia = (1972, 173)  # click_thoat_chon_anh_bia
nutNhanThemSanPham = (2319, 624)  # click_nut_nhan_them_san_pham
nutThemLienKet = (2633, 157)      # click_nut_them_lien_ket
oDanLink = (1994, 364)            # click_va_dan_link
nutNhap = (2257, 730)             # click_nut_nhap
nutChonTatCaSanPham1 = (1957, 1573)  # click_nut_chon_tat_ca_san_pham (click lần 1)
nutChonTatCaSanPham2 = (2464, 1591)  # click_nut_chon_tat_ca_san_pham (click lần 2)
oDanMoTaVideo = (2235, 294)       # click_va_dan_mo_ta_video
nutDongYMoTa = (2609, 174)        # click_nut_dong_y_mo_ta
nutChonAnhBiaMoi1 = (2015, 1487)  # click_chon_anh_bia_moi (click lần 1) 2643
nutChonAnhBiaMoi2 = (2628, 178)   # click_chon_anh_bia_moi (click lần 2)
nutDang = (2357, 1625)            # click_nut_dang
nutTroVeHome = (1962, 155)        # click_tro_ve_home
nutBanNhap = (1986, 1624)         # click_nut_ban_nhap
nutBack = (1957, 165)             # click_nut_back

# Vùng so sánh toàn màn hình cố định
VUNG_SO_SANH_TOAN_MAN_HINH = (1911, 117, 2686 - 1911, 1687 - 117)

def click_mot_lan_vung_nut(vitri_nut, ten_nut, delay=0.5, timeout=2, threshold=0.95):
    """Click 1 lần, chụp và so sánh ảnh vùng quanh nút."""
    vung_nut = (vitri_nut[0] - 50, vitri_nut[1] - 30, 100, 60)
    
    # Chụp ảnh trước khi click
    truoc_file = f"ScreenShot\{ten_nut}_truoc.png"
    sau_file = f"ScreenShot\{ten_nut}_sau.png"
    pyautogui.screenshot(truoc_file, region=vung_nut)
    
    print(f"Đang click nút {ten_nut} tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print(f"Đã click nút {ten_nut}. Chờ phản hồi...")
    
    time.sleep(timeout)
    
    # Chụp ảnh sau khi click
    pyautogui.screenshot(sau_file, region=vung_nut)
    
    # So sánh ảnh
    img1 = imread_unicode(truoc_file)
    img2 = imread_unicode(sau_file)
    
    if img1 is None or img2 is None:
        print(f"❌ Không đọc được ảnh cho nút {ten_nut}.")
        return False
    
    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)
    
    print(f"Độ tương đồng ảnh trước/sau cho nút {ten_nut}: {similarity:.2f}")
    
    if similarity < threshold:
        print(f"✅ Click nút {ten_nut} thành công.")
        return True
    else:
        print(f"⚠️ Nút {ten_nut} vẫn còn, có thể chưa phản hồi.")
        return False

def click_mot_lan_toan_man_hinh(vitri_nut, ten_nut, delay=0.5, timeout=2, threshold=0.95):
    """Click 1 lần, chụp và so sánh ảnh toàn màn hình."""
    # Chụp ảnh trước khi click
    truoc_file = f"ScreenShot\{ten_nut}_truoc.png"
    sau_file = f"ScreenShot\{ten_nut}_sau.png"
    pyautogui.screenshot(truoc_file, region=VUNG_SO_SANH_TOAN_MAN_HINH)
    
    print(f"Đang click nút {ten_nut} tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print(f"Đã click nút {ten_nut}. Chờ phản hồi...")
    
    time.sleep(timeout)
    
    # Chụp ảnh sau khi click
    pyautogui.screenshot(sau_file, region=VUNG_SO_SANH_TOAN_MAN_HINH)
    
    # So sánh ảnh
    img1 = imread_unicode(truoc_file)
    img2 = imread_unicode(sau_file)
    
    if img1 is None or img2 is None:
        print(f"❌ Không đọc được ảnh cho nút {ten_nut}.")
        return False
    
    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)
    
    print(f"Độ tương đồng ảnh trước/sau cho nút {ten_nut}: {similarity:.2f}")
    
    if similarity < threshold:
        print(f"✅ Click nút {ten_nut} thành công.")
        return True
    else:
        print(f"⚠️ Nút {ten_nut} vẫn còn, có thể chưa phản hồi.")
        return False

def click_mot_lan_khong_so_sanh(vitri_nut, ten_nut, delay=0.5):
    """Click 1 lần, không chụp ảnh so sánh."""
    print(f"Đang click nút {ten_nut} tại {vitri_nut} sau {delay} giây...")
    time.sleep(delay)
    pyautogui.moveTo(*vitri_nut, duration=0.2)
    pyautogui.click()
    print(f"✅ Đã click nút {ten_nut}.")

def click_hai_lan(toa_do_1, toa_do_2, ten_nut, delay1=0.5, delay2=0.5, timeout=1, threshold=0.95):
    """Click 2 lần, kiểm tra ảnh sau lần click thứ 2."""
    vung_nut_2 = (toa_do_2[0] - 50, toa_do_2[1] - 30, 100, 60)
    
    # Click lần 1 (không kiểm tra)
    print(f"Click lần 1 nút {ten_nut} tại {toa_do_1}")
    time.sleep(delay1)
    pyautogui.moveTo(*toa_do_1, duration=0.2)
    pyautogui.click()
    
    # Chụp ảnh trước khi click lần 2
    truoc_file = f"ScreenShot\{ten_nut}_truoc.png"
    sau_file = f"ScreenShot\{ten_nut}_sau.png"
    pyautogui.screenshot(truoc_file, region=vung_nut_2)
    
    # Click lần 2
    print(f"Click lần 2 nút {ten_nut} tại {toa_do_2} sau {delay2} giây...")
    time.sleep(delay2)
    pyautogui.moveTo(*toa_do_2, duration=0.2)
    pyautogui.click()
    print(f"Đã click lần 2 nút {ten_nut}. Chờ phản hồi...")
    
    time.sleep(timeout)
    
    # Chụp ảnh sau khi click lần 2
    pyautogui.screenshot(sau_file, region=vung_nut_2)
    
    # So sánh ảnh
    img1 = imread_unicode(truoc_file)
    img2 = imread_unicode(sau_file)
    
    if img1 is None or img2 is None:
        print(f"❌ Không đọc được ảnh cho nút {ten_nut}.")
        return False
    
    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    non_zero = cv2.countNonZero(thresh)
    total_pixels = diff.shape[0] * diff.shape[1]
    similarity = 1 - (non_zero / total_pixels)
    
    print(f"Độ tương đồng ảnh trước/sau cho nút {ten_nut}: {similarity:.2f}")
    
    if similarity < threshold:
        print(f"✅ Click nút {ten_nut} thành công.")
        return True
    else:
        print(f"⚠️ Giao diện chưa thay đổi rõ ràng cho nút {ten_nut}.")
        return False

# Các hàm khác giữ nguyên
def click_va_dan_link(vitri_o=oDanLink, doan_text="", ten_nut="dán link"):
    """Click và dán link/mô tả."""
    print(f"Click tại {vitri_o} và {ten_nut}...")
    pyperclip.copy(doan_text)
    pyautogui.moveTo(*vitri_o, duration=0.2)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")
    print(f"✅ Đã {ten_nut} thành công.")

def chup_anh_so_video(filename=f"ScreenShot\anhSoCuaVideo.png"):
    """Chụp ảnh số của video."""
    x1, y1 = nutSoVideo
    x2, y2 = 2369, 880
    width = x2 - x1
    height = y2 - y1
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot.save(filename)
    print(f"✅ Đã lưu ảnh vào: {filename}")

# Hàm nhan_dien_so_tu_anh giữ nguyên
def nhan_dien_so_tu_anh(duong_dan_anh):
    try:
        img = imread_unicode(duong_dan_anh)
        h, w = img.shape[:2]
        left = int(w * 0.01)
        right = int(w * 0.99)
        img = img[:, left:right]
        padding = 50
        img = cv2.copyMakeBorder(
            img, padding, padding, padding, padding,
            cv2.BORDER_CONSTANT, value=[255, 255, 255]
        )
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) < 30:
                cv2.drawContours(thresh, [cnt], -1, 0, -1)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        inverted = cv2.bitwise_not(closed)
        scale_up = cv2.resize(inverted, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(f"ScreenShot\processed.png", scale_up)
        config1 = '--psm 8 -c tessedit_char_whitelist=0123456789'
        text1 = pytesseract.image_to_string(scale_up, config=config1)
        so1 = ''.join(filter(str.isdigit, text1))
        if so1:
            print(f"[OCR Lần 1 - psm8]: '{text1.strip()}' ➤ Kết quả: {so1}")
            return so1
        config2 = '--psm 6 -c tessedit_char_whitelist=0123456789'
        text2 = pytesseract.image_to_string(scale_up, config=config2)
        so2 = ''.join(filter(str.isdigit, text2))
        print(f"[OCR Lần 2 - psm7]: '{text2.strip()}' ➤ Kết quả: {so2}")
        return so2
    except Exception as e:
        print(f"❌ Lỗi OCR: {e}")
        return None

# Hàm thử lại click 
def thu_lai_click(func, so_lan_thu=2, delay=1):
    """Thử lại click nếu thất bại."""
    for lan in range(so_lan_thu):
        if func():
            return True
        print(f"⚠️ Click thất bại lần {lan + 1}, thử lại...")
        time.sleep(delay)
    print("❌ Đã thử nhiều lần nhưng vẫn thất bại.")
    return False

# ====================== CHỌN VIDEO VỚI LOGIC DỊCH TỌA ĐỘ ======================
so_lan_click_video = 0
vitri_chon_video = [2001, 415]
cuon_chuot_y = 0

def click_chon_video(delay=0.5, timeout=3, threshold=0.95):
    """
    Click chọn video theo hàng 4-cột.
    Trước mỗi lần click:
      - Luôn cuộn đến vị trí tổng = block * 180,
        với block = so_lan_click_video // 4 (hàng thứ mấy, bắt đầu từ 0).
      - Mỗi hàng có 4 video, vị trí X = base + (so_lan_click_video % 4) * 200
    """
    global vitri_chon_video, so_lan_click_video, cuon_chuot_y

    time.sleep(0.5)

    # Khởi tạo lần đầu
    if so_lan_click_video == 0:
        vitri_chon_video = list(nutChonVideo)
        cuon_chuot_y = 0

    # Tính hàng hiện tại
    block = so_lan_click_video // 4
    muc_cuon = block * 180

    # # Nếu mức cuộn hiện tại khác mức mong muốn -> cuộn tới đó
    # if cuon_chuot_y != muc_cuon:
    #     delta = muc_cuon - cuon_chuot_y
    #     pyautogui.scroll(-delta)
    #     cuon_chuot_y = muc_cuon
    #     print(f"🔃 Cuộn đến {cuon_chuot_y}px (hàng {block}) trước khi click video {so_lan_click_video + 1}")
    #     time.sleep(0.4)

    print("MUC CUON ======= ", muc_cuon)
    pyautogui.scroll(-muc_cuon)
    time.sleep(0.4)

    # Cập nhật vị trí click theo cột trong hàng
    vitri_chon_video = [nutChonVideo[0] + (so_lan_click_video % 4) * 200, nutChonVideo[1]]

    vitri_nut = tuple(vitri_chon_video)
    print(f"🎯 Click 'Chọn video' tại {vitri_nut} (lần thứ {so_lan_click_video + 1})")

    # Thực hiện click
    result = click_mot_lan_toan_man_hinh(vitri_nut, f"Chọn video {so_lan_click_video + 1}", delay, timeout, threshold)

    if result:
        so_lan_click_video += 1

    return result




def click_va_dan_mo_ta_video(vitri_o=(2235, 294), doan_text=""):
    print(f"Click tại {vitri_o} và them mo ta...")
    pyperclip.copy(doan_text)          # Copy vào clipboard
    pyautogui.moveTo(*vitri_o, duration=0.2)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")      # Dán từ clipboard
    print("✅ Đã dán link thành công.")


import openpyxl

def doc_cot_dau_tien_xlsx(file_path):
    """
    Đọc cột đầu tiên từ file .xlsx, bắt đầu từ hàng 2, dừng khi gặp ô rỗng.
    Trả về danh sách các giá trị trong cột đầu tiên.
    
    Parameters:
    - file_path (str): Đường dẫn đến file .xlsx
    
    Returns:
    - listLinkSP (list): Danh sách các giá trị trong cột đầu tiên
    """
    listLinkSP = []
    
    try:
        # Mở file Excel
        workbook = openpyxl.load_workbook(file_path)
        # Lấy sheet đầu tiên
        sheet = workbook.active
        
        # Đọc từ hàng 2, cột 1 (A)
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1, values_only=True):
            # Lấy giá trị ô đầu tiên trong hàng
            cell_value = row[0]
            
            # Nếu ô rỗng, dừng đọc
            if cell_value is None or str(cell_value).strip() == "":
                break
                
            # Thêm giá trị vào danh sách
            listLinkSP.append(str(cell_value).strip())
        
        print(f"✅ Đã đọc {len(listLinkSP)} giá trị từ cột đầu tiên.")
        return listLinkSP
    
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {file_path}")
        return []
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")
        return []



def DangVideo(index):
    """
    Đăng video thứ index, trả về False nếu bất kỳ bước nào thất bại.
    
    Parameters:
    - index (int): Chỉ số video trong danh sách
    - moTaVideo (str): Mô tả video để dán
    - listLinkSP (list): Danh sách link sản phẩm
    
    Returns:
    - bool: True nếu tất cả bước thành công, False nếu có bước thất bại
    """
    print(f"======================================== DANG VIDEO THU {index + 1} ======================================")

    # Bước 1: Click nút Đăng video
    if not click_mot_lan_vung_nut(nutDangVideo, "Nut Dang Video"):
        return False

    # Bước 2: Click nút Thư viện
    if not click_mot_lan_toan_man_hinh(nutThuVien, "Nut Thu Vien Anh"):
        return False

    # Bước 3: Click chọn video (theo thứ tự và cuộn)
    if not click_chon_video():
        return False


    # Bước 4: Click nút Tiếp theo (lần 1)
    click_mot_lan_khong_so_sanh(nutTiepTheo, "Nut Tiep Theo 1")
    
    time.sleep(0.5)

    # Bước 5: Click nút Tiếp theo (lần 2)
    if not click_mot_lan_toan_man_hinh(nutTiepTheo, "Nut Tiep Theo 2"):
        return False

    # Bước 6: Click nút Chọn ảnh bìa
    if not click_mot_lan_toan_man_hinh(nutChonAnhBia, "Nut Chon Anh Bia"):
        return False

    # Bước 7: Click chọn ảnh bìa mới (với tọa độ ngẫu nhiên cho lần click 1)
    nutChonAnhBiaMoi1 = (random.randint(2015, 2643), 1487)
    if not click_hai_lan(nutChonAnhBiaMoi1, nutChonAnhBiaMoi2, "Nut Chon Anh Bia Moi"):
        return False

    time.sleep(0.5)

    # Bước 8: Dán mô tả video
    click_va_dan_mo_ta_video(doan_text=moTaVideo)

    time.sleep(0.1)

    # Bước 9: Click nút Đồng ý nhập mô tả
    if not click_mot_lan_vung_nut(nutDongYMoTa, "Nut Dong Y Nhap Mo Ta"):
        return False

    # Bước 10: Click nút Nhận thêm sản phẩm
    if not click_mot_lan_vung_nut(nutNhanThemSanPham, "Nut Nhan Them San Pham"):
        return False

    # Bước 11: Click nút Thêm liên kết
    if not click_mot_lan_toan_man_hinh(nutThemLienKet, "Nut Them Lien Ket"):
        return False

    # Bước 12: Dán link sản phẩm
    click_va_dan_link(oDanLink, listLinkSP[index + 1])

    # Bước 13: Click nút Nhập link
    if not click_mot_lan_toan_man_hinh(nutNhap, "Nut Nhap Link"):
        if not click_mot_lan_toan_man_hinh(nutNhap, "Nut Nhap Link"):
            if not click_mot_lan_toan_man_hinh(nutNhap, "Nut Nhap Link"):
                return False

    # Bước 14: Click chọn tất cả sản phẩm
    if not click_hai_lan(nutChonTatCaSanPham1, nutChonTatCaSanPham2, "Nut Chon Tat Ca San Pham"):
        return False

    # Bước 15: Click nút Đăng
    if not click_mot_lan_toan_man_hinh(nutDang, "Nut Dang"):
        return False

    time.sleep(3)

    # Bước 16: Click trở về trang Home
    if not click_mot_lan_toan_man_hinh(nutTroVeHome, "Nut Tro Ve Trang Home"):
        return False

    print(f"✅ Hoan tat dang video thu {index}")
    return True

#ShopeeCreator #ShopeeStyle #ShopeeVideo #LuotVuiMuaLien #VideohangDoiSong #VideohangTieuDung #VideohangGiaDung Xịn lắmm 😻
    


#DangVideo()

# Ví dụ sử dụng:
file_path = r"C:\Users\84765\Desktop\MMO\Shopee\ShopeeVy\CanXuLy\mainBoard\1.xlsx"

listLinkSP = doc_cot_dau_tien_xlsx(file_path)
#Mo ta video
moTaVideo = """mainboard bo mạch chủ pc chất lượng.  #ShopeeCreator #ShopeeStyle #ShopeeVideo #LuotVuiMuaLien  
#MainBoard #Pc"""
linkSP = ""


print(len(listLinkSP))

for i in range(len(listLinkSP) - 1):
    if not DangVideo(i):
        break
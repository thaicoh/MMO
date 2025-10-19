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
import openpyxl
import numpy as np
import cv2
from ChupSoLuongSanPham import ocrSoLuongSanPham

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

VUNG_SO_SANH_TOAN_MAN_HINH = (1911, 117, 2686 - 1911, 1687 - 117) # Vùng so sánh toàn màn hình cố định

def imread_unicode(path):
    """Đọc ảnh có tên Unicode (có dấu tiếng Việt)."""
    try:
        data = np.fromfile(path, dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"⚠️ Lỗi đọc ảnh '{path}': {e}")
        return None

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

def click_va_dan_link(vitri_o=oDanLink, doan_text="", ten_nut="dán link"):
    """Click và dán link/mô tả."""
    print(f"Click tại {vitri_o} và {ten_nut}...")
    pyperclip.copy(doan_text)
    pyautogui.moveTo(*vitri_o, duration=0.2)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")
    print(f"✅ Đã {ten_nut} thành công.")

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

def doc_link_tu_txt(file_path):
    """
    Đọc file .txt, mỗi dòng là một link sản phẩm.
    Bỏ qua dòng trống và khoảng trắng dư thừa.
    Trả về danh sách các link.

    Parameters:
    - file_path (str): Đường dẫn đến file .txt

    Returns:
    - listLinkSP (list): Danh sách link sản phẩm
    """
    listLinkSP = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                link = line.strip()
                if not link:  # Nếu dòng trống thì bỏ qua
                    break
                listLinkSP.append(link)

        print(f"✅ Đã đọc {len(listLinkSP)} link sản phẩm từ file TXT.")
        return listLinkSP

    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {file_path}")
        return []
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")
        return []

def get_links(listLinkSP, start_index, so_luong):
    """
    Lấy ra một chuỗi các link sản phẩm, cách nhau bằng khoảng trắng.
    Bắt đầu tại vị trí start_index, lấy số lượng là so_luong.

    Parameters:
    - listLinkSP (list): Danh sách tất cả link sản phẩm
    - start_index (int): Vị trí bắt đầu (0-based index)
    - so_luong (int): Số lượng link cần lấy

    Returns:
    - str: Chuỗi các link nối với nhau bằng khoảng trắng
    """
    if not listLinkSP:
        print("❌ Danh sách link sản phẩm rỗng.")
        return ""

    if start_index < 0 or start_index >= len(listLinkSP):
        start_index = start_index - len(listLinkSP)

    # Lấy danh sách con
    end_index = start_index + so_luong
    list_con = listLinkSP[start_index:end_index]

    # Ghép thành chuỗi
    chuoi_link = " ".join(list_con)

    print(f"✅ Lấy {len(list_con)} link (từ {start_index} đến {end_index - 1}).")
    return chuoi_link

def ghi_log_link(list_link):
    """
    Ghi danh sách link đã dán vào file log.
    Mỗi link một dòng, ghi nối tiếp vào file.
    """
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for link in list_link:
                f.write(link + "\n")
        print(f"📝 Đã ghi {len(list_link)} link vào file log '{LOG_FILE}'.")
    except Exception as e:
        print(f"❌ Lỗi khi ghi file log: {e}")

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

def DangVideo(index, indexLinks):

    soLuongLinkCanDan = 6

    print(f"======================================== DANG VIDEO THU {index + 1} ======================================")
    print("indexLink end trong=", indexLinks)


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
    while True:
        # 1️⃣ Lấy nhóm link cần dán
        list_dan = get_links(listLinkSP, indexLinks, soLuongLinkCanDan).split(" ")

        # 2️⃣ Dán link
        click_va_dan_link(oDanLink, " ".join(list_dan))

        time.sleep(2)

        # 3️⃣ Click nút nhập link (thử 3 lần)
        for _ in range(3):
            if click_mot_lan_toan_man_hinh(nutNhap, "Nut Nhap Link"):
                break
        else:
            print("❌ Lỗi click_mot_lan_toan_man_hinh, bỏ qua vòng này")
            continue
        

        if chup_va_so_sanh_da_chon_tat_ca_chua(r"C:\Users\84765\Desktop\AutoClick\mauOCLickChonTatCa.png"):
            print("Hai ảnh giống nhau!")
            indexLinks += len(list_dan)
            # 6️⃣ Ghi log các link đã dán thành công
            ghi_log_link(list_dan)

            continue
        else:
            # 4️⃣ Click chọn tất cả sản phẩm
            click_mot_lan_khong_so_sanh(nutChonTatCaSanPham1, "Nut Chon Tat Ca San Pham")
        
        time.sleep(2)

        # 5️⃣ OCR đếm sản phẩm
        try:
            so_nhan_dien = int(ocrSoLuongSanPham())
        except:
            so_nhan_dien = 0

        print(f"Số nhận diện được: {so_nhan_dien}")

        time.sleep(1)

        # 6️⃣ Ghi log các link đã dán thành công
        ghi_log_link(list_dan)

        # 7️⃣ Điều kiện dừng hoặc tiếp tục
        if so_nhan_dien == 6:
            indexLinks += len(list_dan)
            break
        elif so_nhan_dien < 6:
            soLuongLinkCanDan = 6 - so_nhan_dien
            indexLinks += len(list_dan)
            print(f"⚠️ Chưa đủ ({so_nhan_dien}/6) → Lấy thêm {soLuongLinkCanDan} link tiếp theo (index {indexLinks}).")
        else:
            print("⚠️ Nhận diện vượt mức (sai logic), dừng để kiểm tra.")
            break

    # # Bước 13: Click nút Nhập link
    # if not click_mot_lan_toan_man_hinh(nutNhap, "Nut Nhap Link"):
    #     if not click_mot_lan_toan_man_hinh(nutNhap, "Nut Nhap Link"):
    #         if not click_mot_lan_toan_man_hinh(nutNhap, "Nut Nhap Link"):
    #             return False

    # # Bước 14: Click chọn tất cả sản phẩm
    # if not click_hai_lan(nutChonTatCaSanPham1, nutChonTatCaSanPham2, "Nut Chon Tat Ca San Pham"):
    #     return False

    # Bước 15: Click nút Đăng
    if not click_mot_lan_toan_man_hinh(nutChonTatCaSanPham2, "nutChonTatCaSanPham2"):
        return False
    
    # Bước 15: Click nút Đăng
    if not click_mot_lan_toan_man_hinh(nutDang, "Nut Dang"):
        return False

    time.sleep(3)

    # Bước 16: Click trở về trang Home
    if not click_mot_lan_toan_man_hinh(nutTroVeHome, "Nut Tro Ve Trang Home"):
        return False

    print(f"✅ Hoan tat dang video thu {index + 1}")
    print("indexLink end trong=", indexLinks)
    return True, indexLinks

# Ví dụ sử dụng:
file_path = r"C:\Users\84765\Downloads\manhinhxiaomi\link_san_pham.txt"
LOG_FILE = r"C:\Users\84765\Downloads\manhinhxiaomi\link_da_dan_mainboard2.txt"

moTaVideo = """Mình hình thay thế cho điện thoại xiaomi.  #ShopeeCreator #ShopeeStyle #ShopeeVideo #LuotVuiMuaLien  
#xiaomi #manhinh"""

soLuongDang = 46

listLinkSP = doc_link_tu_txt(file_path)
#Mo ta video
linkSP = ""

indexLinks = 0
soLuongLinkCanDan = 6


for i in range(soLuongDang):
    ket_qua, indexLinks = DangVideo(i, indexLinks)

    if(indexLinks >= len(listLinkSP)):
        print("da dang tat ca link SP")
        break

    if not ket_qua:
        break





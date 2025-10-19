from PIL import ImageGrab
import easyocr
import os
import re
import warnings
warnings.filterwarnings("ignore")

def ocrSoLuongSanPham(bbox = (2261, 1545, 2595, 1602)):
    
    file_path = f"ScreenShot\hinh_anh_so_Video.png"
    screenshot = ImageGrab.grab(bbox=bbox)
    screenshot.save(file_path)

    # Kiểm tra file và nhận diện
    if os.path.exists(file_path):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(file_path)
        for result in results:
            text = result[1]
            digits = re.findall(r'\d+', text)

            if digits:
                return digits[0]
            else:
                return 0

    else:
        return -1
    

# print("Số nhận diện được: " + ocrSoLuongSanPham())

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ⚙️ Cấu hình trình duyệt Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--headless")  # Bỏ comment nếu không muốn hiện trình duyệt

driver = webdriver.Chrome(options=chrome_options)

# 📖 Đọc file TXT chứa các link TikTok
with open(r"C:\Users\84765\Downloads\tiktok_links (3).txt", "r", encoding="utf-8") as f:
    links = [line.strip() for line in f if line.strip()]

# 📄 Mở file kết quả để ghi
output = open("ketqua.txt", "w", encoding="utf-8")

# 🧭 Mở ssstik.io
driver.get("https://ssstik.io/")

for index, tiktok_url in enumerate(links, start=1):
    print(f"📥 [{index}] Đang xử lý: {tiktok_url}")

    try:
        # ⏳ Chờ input khả dụng
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "main_page_text")))

        # ✏️ Gửi link vào input
        input_box = driver.find_element(By.ID, "main_page_text")
        driver.execute_script("arguments[0].value = '';", input_box)
        input_box.send_keys(tiktok_url)

        # 🖱️ Submit
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        # ⏳ Chờ xử lý video
        time.sleep(7)

        # 🔍 Tìm thẻ <a> chứa link ssstik
        a_tags = driver.find_elements(By.TAG_NAME, "a")
        video_link = None
        for a in a_tags:
            href = a.get_attribute("href")
            if href and "https://tikcdn.io/ssstik/" in href and href.endswith(".mp4"):
                video_link = href
                break

        if video_link:
            print(f"✅ Link video: {video_link}")
            output.write(video_link + "\n")
        else:
            print("❌ Không tìm thấy link .mp4")

    except Exception as e:
        print("⚠️ Lỗi:", e)

# ✅ Đóng file và trình duyệt
output.close()
driver.quit()
print("🎉 Đã xong, kết quả lưu vào 'ketqua.txt'")
import csv
import os

# Thư mục chứa các file CSV
folder_path = r"C:\Users\84765\Downloads\pc_gaming"  # Đổi thành thư mục của bạn
output_file = folder_path+"\link_san_pham.txt"

# Danh sách lưu tất cả link sản phẩm
all_links = []

# Duyệt qua tất cả file trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                link = row.get('Link sản phẩm')
                if link:
                    all_links.append(link)

# Ghi toàn bộ link ra file TXT
with open(output_file, mode='w', encoding='utf-8') as txtfile:
    for link in all_links:
        txtfile.write(link + '\n')

print(f"Đã xuất {len(all_links)} link sản phẩm từ {folder_path} vào {output_file}")
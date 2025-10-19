import openpyxl

# Đường dẫn tới file Excel
excel_file = r"C:\Users\84765\Desktop\MMO\Shopee\ShopeeVy\CanXuLy\mainBoard\test.xlsx"

# Mở workbook
wb = openpyxl.load_workbook(excel_file)
ws = wb.active

# Chuyển generator thành danh sách các cột
columns = list(ws.iter_cols(values_only=True))

# Duyệt qua từng cột
for col_index, col in enumerate(columns, start=1):
    # Bỏ qua cột rỗng
    if all(cell is None for cell in col):
        continue

    # Tạo tên file txt theo chỉ số cột
    txt_filename = f'column_{col_index}.txt'

    # Ghi dữ liệu vào file txt
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for cell in col:
            if cell:
                # Tách các link bằng khoảng trắng
                links = str(cell).strip().split()
                for link in links:
                    f.write(link + '\n')

print("Đã tách và ghi từng link ra file txt theo từng cột.")



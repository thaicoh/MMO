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

duong_dan = r"C:\Users\84765\Downloads\9_output_final_15.xlsx"
data = doc_file_va_tra_ve_dict_so_link(duong_dan)

# In kết quả
for so, link in data.items():
    print(f"{so} ➤ {link}")

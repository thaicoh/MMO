import pyautogui
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from pynput import mouse

class ToaDoSelector:
    def __init__(self):
        self.nuts = [
            ("nutDangVideo", "Click nút đăng video"),
            ("nutThuVien", "Click nút thư viện"),
            ("nutChonVideo", "Click chọn video (base)"),
            ("nutTiepTheo", "Click nút tiếp theo"),
            ("nutChonAnhBia", "Click chọn ảnh bìa"),
            ("nutSoVideo", "Chụp ảnh số video"),
            ("nutThoatChonAnhBia", "Thoát chọn ảnh bìa"),
            ("nutNhanThemSanPham", "Nhận thêm sản phẩm"),
            ("nutThemLienKet", "Thêm liên kết"),
            ("oDanLink", "Ô dán link"),
            ("nutNhap", "Nút nhập"),
            ("nutChonTatCaSanPham1", "Chọn tất cả SP (click 1)"),
            ("nutChonTatCaSanPham2", "Chọn tất cả SP (click 2)"),
            ("oDanMoTaVideo", "Ô dán mô tả video"),
            ("nutDongYMoTa", "Đồng ý mô tả"),
            ("nutChonAnhBiaMoi1", "Chọn ảnh bìa mới (click 1)"),
            ("nutChonAnhBiaMoi2", "Chọn ảnh bìa mới (click 2)"),
            ("nutDang", "Nút đăng"),
            ("nutTroVeHome", "Trở về Home"),
            ("nutBanNhap", "Bàn nhập"),
            ("nutBack", "Nút Back")
        ]
        self.toa_do_dict = {}
        self.current_nut = None
        self.running = False
        self.mouse_listener = None
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        self.root.title("🖱️ CHỌN NÚT & CLICK PHẢI LẤY TỌA ĐỘ")
        self.root.geometry("600x800")
        self.root.configure(bg='#2c3e50')
        
        # Tiêu đề
        title = tk.Label(self.root, text="🖱️ CHỌN NÚT ĐỂ LẤY TỌA ĐỘ", 
                         font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=10)
        
        # Frame danh sách nút
        self.nut_frame = tk.Frame(self.root, bg='#34495e')
        self.nut_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.check_vars = {}
        self.coord_vars = {}
        self.check_buttons = {}
        for ten_nut, mo_ta in self.nuts:
            frame = tk.Frame(self.nut_frame, bg='#34495e')
            frame.pack(fill='x', pady=2)
            
            var = tk.BooleanVar()
            self.check_vars[ten_nut] = var
            chk = tk.Checkbutton(frame, text=f"{ten_nut}  # {mo_ta}", 
                                 variable=var, bg='#34495e', fg='white', 
                                 selectcolor='#27ae60', font=('Consolas', 9), 
                                 command=lambda tn=ten_nut: self.on_check(tn))
            chk.pack(side='left', padx=5)
            
            coord_var = tk.StringVar(value="")
            self.coord_vars[ten_nut] = coord_var
            coord_label = tk.Label(frame, textvariable=coord_var, 
                                   bg='#34495e', fg='yellow', font=('Consolas', 9))
            coord_label.pack(side='right', padx=5)
            
            self.check_buttons[ten_nut] = chk
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg='#2c3e50')
        btn_frame.pack(fill='x', pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="🖱️ BẮT ĐẦU - CLICK PHẢI", 
                                   font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                                   command=self.start_listener, width=25)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ DỪNG", 
                                  font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                                  command=self.stop_listener, width=15, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        self.gen_code_btn = tk.Button(btn_frame, text="💻 TẠO CODE", 
                                      font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                      command=self.generate_code, width=15)
        self.gen_code_btn.pack(side='left', padx=5)
        
        # Progress
        self.progress_var = tk.StringVar(value="⏸️ TICK 1 NÚT → BẮT ĐẦU → CLICK PHẢI")
        progress_label = tk.Label(self.root, textvariable=self.progress_var, 
                                  font=('Arial', 12), bg='#2c3e50', fg='yellow')
        progress_label.pack(pady=10)
        
        # Code area
        code_frame = tk.LabelFrame(self.root, text="💻 CODE SẴN SÀNG:", 
                                   font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        code_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.code_text = scrolledtext.ScrolledText(code_frame, height=6, font=('Consolas', 10), 
                                                   bg='#1e1e1e', fg='#00ff00')
        self.code_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def on_check(self, ten_nut):
        """Xử lý khi tick checkbox"""
        if self.check_vars[ten_nut].get() and self.current_nut is None:
            for tn, var in self.check_vars.items():
                if tn != ten_nut:
                    var.set(False)
            self.current_nut = ten_nut
            self.progress_var.set(f"🖱️ CHỜ CLICK PHẢI: {ten_nut}")
        elif not self.check_vars[ten_nut].get() and self.current_nut == ten_nut:
            self.current_nut = None
            self.progress_var.set("⏸️ TICK 1 NÚT KHÁC ĐỂ TIẾP TỤC")
            
    def on_click(self, x, y, button, pressed):
        """Detect click phải"""
        if pressed and button == mouse.Button.right and self.running and self.current_nut:
            self.root.after(0, lambda: self.handle_right_click(int(x), int(y)))
            return False
            
    def handle_right_click(self, x, y):
        """Xử lý click phải và cập nhật tọa độ"""
        if self.current_nut:
            self.toa_do_dict[self.current_nut] = (x, y)
            self.coord_vars[self.current_nut].set(f"({x}, {y})")
            self.check_buttons[self.current_nut].deselect()
            self.check_vars[self.current_nut].set(False)
            self.current_nut = None
            self.progress_var.set("✅ ĐÃ LẤY TỌA ĐỘ. TICK NÚT KHÁC ĐỂ TIẾP TỤC")
            
            # Kiểm tra xem còn nút nào chưa lấy tọa độ không
            if all(ten_nut in self.toa_do_dict for ten_nut, _ in self.nuts):
                self.stop_listener()
                messagebox.showinfo("🎉 HOÀN TẤT", f"Đã lấy tọa độ cho {len(self.toa_do_dict)} nút!")
                
    def start_listener(self):
        """Bắt đầu lắng nghe"""
        if not self.current_nut:
            messagebox.showerror("❌ LỖI", "VUI LÒNG TICK 1 NÚT TRƯỚC!")
            return
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.gen_code_btn.config(state='disabled')
        self.progress_var.set(f"🖱️ CHỜ CLICK PHẢI: {self.current_nut}")
        
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()
        
    def stop_listener(self):
        """Dừng lắng nghe"""
        self.running = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.gen_code_btn.config(state='normal')
        self.current_nut = None
        self.progress_var.set("⏹️ ĐÃ DỪNG. TICK NÚT ĐỂ TIẾP TỤC HOẶC TẠO CODE")
        
    def generate_code(self):
        """Tạo code"""
        if not self.toa_do_dict:
            messagebox.showerror("❌ LỖI", "CHƯA CÓ TỌA ĐỘ NÀO!")
            return
            
        code = "# 📍 TỌA ĐỘ CỐT LÕI (TỰ ĐỘNG TẠO)\n\n"
        for ten_nut, mo_ta in self.nuts:
            toa = self.toa_do_dict.get(ten_nut)
            if toa:
                code += f"{ten_nut:<20} = {str(toa)}  # {mo_ta}\n"  # Chuyển tuple thành chuỗi
            else:
                code += f"{ten_nut:<20} = ()  # {mo_ta}\n"
        code += "\n" + "="*50 + "\n"
        
        self.code_text.delete('1.0', tk.END)
        self.code_text.insert('1.0', code)
        
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        messagebox.showinfo("✅ THÀNH CÔNG", f"ĐÃ TẠO CODE {len(self.toa_do_dict)} NÚT!\n📋 ĐÃ COPY - DÁN NGAY!")
        
    def run(self):
        pyautogui.FAILSAFE = False
        messagebox.showinfo("🚀 SẴN SÀNG", 
                           "1️⃣ TICK 1 NÚT\n"
                           "2️⃣ BẮT ĐẦU\n"
                           "3️⃣ CLICK PHẢI ĐỂ LẤY TỌA ĐỘ\n"
                           "4️⃣ TICK NÚT KHÁC ĐỂ TIẾP TỤC")
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.root.mainloop()

if __name__ == "__main__":
    app = ToaDoSelector()
    app.run()
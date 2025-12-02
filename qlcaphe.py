import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="QLcaphe"
    )

# ====== Căn giữa ======
def center_window(win, w=950, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ====== Format tiền VND ======
def format_vnd(value):
    try:
        return f"{int(value):,} VND"
    except:
        return value

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý cà phê")
center_window(root)
root.resizable(False, False)

tk.Label(root, text="QUẢN LÝ CÀ PHÊ", font=("Arial", 20, "bold")).pack(pady=10)
frame = tk.Frame(root)
frame.pack(fill="x", padx=10)

# ====== Load bảng phụ ======
def load_loai():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT maloai, tenloai FROM loaicaphe")
    data = cur.fetchall()
    conn.close()
    return data

def load_ncc():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT mancc, tenncc FROM nhacungcap")
    data = cur.fetchall()
    conn.close()
    return data

# ====== Hàm căn trái cho grid ======
def left_grid(widget, row, column, width=None):
    if width:
        widget.config(width=width)
    widget.grid(row=row, column=column, padx=5, pady=5, sticky="w")

# ====== INPUT ======
tk.Label(frame, text="Mã cà phê").grid(row=0, column=0, sticky="w")
entry_ma = tk.Entry(frame)
left_grid(entry_ma, 0, 1, 15)

tk.Label(frame, text="Tên cà phê").grid(row=0, column=2, sticky="w")
entry_ten = tk.Entry(frame)
left_grid(entry_ten, 0, 3, 25)

tk.Label(frame, text="Loại").grid(row=1, column=0, sticky="w")
cbb_loai = ttk.Combobox(frame, state="readonly")
left_grid(cbb_loai, 1, 1, 25)

tk.Label(frame, text="Giá (VND)").grid(row=1, column=2, sticky="w")
entry_gia = tk.Entry(frame)
left_grid(entry_gia, 1, 3, 15)

tk.Label(frame, text="Số lượng").grid(row=2, column=0, sticky="w")
entry_sl = tk.Entry(frame)
left_grid(entry_sl, 2, 1, 15)

tk.Label(frame, text="Ngày nhập").grid(row=2, column=2, sticky="w")
date_entry = DateEntry(frame, width=12, date_pattern="yyyy-mm-dd")
left_grid(date_entry, 2, 3)

tk.Label(frame, text="Nhà cung cấp").grid(row=3, column=0, sticky="w")
cbb_ncc = ttk.Combobox(frame, state="readonly")
left_grid(cbb_ncc, 3, 1, 25)

def load_combobox():
    cbb_loai["values"] = [f"{a} - {b}" for a,b in load_loai()]
    cbb_ncc["values"] = [f"{a} - {b}" for a,b in load_ncc()]
load_combobox()

# ====== TREEVIEW ======
columns = ("ma", "ten", "tenloai", "gia", "soluong", "ngaynhap", "ncc")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
titles = ["Mã", "Tên", "Loại", "Giá (VND)", "SL", "Ngày", "Nhà CC"]
widths = [80, 150, 120, 120, 60, 100, 150]
for col, tit, w in zip(columns, titles, widths):
    tree.heading(col, text=tit)
    tree.column(col, width=w, anchor="w")  # căn trái
tree.pack(padx=10, pady=10, fill="both")

# ====== CLEAR ======
def clear_input():
    entry_ma.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    entry_gia.delete(0, tk.END)
    entry_sl.delete(0, tk.END)
    cbb_loai.set("")
    cbb_ncc.set("")
    date_entry.set_date("2000-01-01")

# ====== LOAD DATA ======
def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.macaphe, c.tencaphe, l.tenloai, c.gia,
               c.soluong, c.ngaynhap, n.tenncc
        FROM caphe c
        LEFT JOIN loaicaphe l ON c.maloai=l.maloai
        LEFT JOIN nhacungcap n ON c.mancc=n.mancc
    """)
    for row in cur.fetchall():
        row = list(row)
        row[3] = format_vnd(row[3])
        tree.insert("", tk.END, values=row)
    conn.close()

# ====== THÊM ======
def them():
    ma = entry_ma.get()
    ten = entry_ten.get()
    gia = entry_gia.get()
    sl = entry_sl.get()
    ngay = date_entry.get()
    maloai = cbb_loai.get().split(" - ")[0]
    mancc = cbb_ncc.get().split(" - ")[0]
    if ma=="" or ten=="":
        messagebox.showwarning("Thiếu dữ liệu","Nhập mã và tên")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO caphe(macaphe,tencaphe,gia,soluong,ngaynhap,maloai,mancc) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (ma,ten,gia,sl,ngay,maloai,mancc))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

# ====== XÓA ======
def xoa():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn","Chọn sản phẩm!")
        return
    ma = tree.item(sel)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM caphe WHERE macaphe=%s",(ma,))
    conn.commit()
    conn.close()
    load_data()

# ====== SỬA ======
def sua():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn","Chọn 1 dòng để sửa")
        return
    values = tree.item(sel)["values"]
    entry_ma.delete(0, tk.END)
    entry_ma.insert(0, values[0])
    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, values[1])
    entry_gia.delete(0, tk.END)
    entry_gia.insert(0, values[3].replace(" VND","").replace(",",""))
    entry_sl.delete(0, tk.END)
    entry_sl.insert(0, values[4])
    date_entry.set_date(values[5])
    for v in cbb_loai["values"]:
        if values[2] in v:
            cbb_loai.set(v)
    for v in cbb_ncc["values"]:
        if values[6] in v:
            cbb_ncc.set(v)

# ====== LƯU ======
def luu():
    ma = entry_ma.get()
    ten = entry_ten.get()
    gia = entry_gia.get()
    sl = entry_sl.get()
    ngay = date_entry.get()
    maloai = cbb_loai.get().split(" - ")[0]
    mancc = cbb_ncc.get().split(" - ")[0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE caphe SET tencaphe=%s, gia=%s, soluong=%s, ngaynhap=%s, maloai=%s, mancc=%s WHERE macaphe=%s",
                (ten, gia, sl, ngay, maloai, mancc, ma))
    conn.commit()
    conn.close()
    load_data()
    clear_input()

# ====== XUẤT EXCEL ======
def xuat_excel():
    wb = Workbook()
    ws = wb.active
    ws.append(["Mã cà phê","Tên cà phê","Loại","Giá (VND)","Số lượng","Ngày nhập","Nhà cung cấp"])
    for row in tree.get_children():
        ws.append(tree.item(row)["values"])
    for col in ws.columns:
        for cell in col:
            cell.alignment = Alignment(horizontal="left")
    filename = f"caphe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb.save(filename)
    messagebox.showinfo("Thông báo",f"Đã xuất file: {filename}")

# ====== BUTTON ======
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)
tk.Button(frame_btn,text="Thêm",width=10,command=them).grid(row=0,column=0,padx=5)
tk.Button(frame_btn,text="Sửa",width=10,command=sua).grid(row=0,column=1,padx=5)
tk.Button(frame_btn,text="Lưu",width=10,command=luu).grid(row=0,column=2,padx=5)
tk.Button(frame_btn,text="Hủy",width=10,command=clear_input).grid(row=0,column=3,padx=5)
tk.Button(frame_btn,text="Xóa",width=10,command=xoa).grid(row=0,column=4,padx=5)
tk.Button(frame_btn,text="Xuất Excel",width=10,command=xuat_excel).grid(row=0,column=5,padx=5)
tk.Button(frame_btn,text="Thoát",width=10,command=root.quit).grid(row=0,column=6,padx=5)

# ====== LOAD ======
load_data()
root.mainloop()

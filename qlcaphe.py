import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="QLcaphe"
    )

# ====== Căn giữa ======
def center_window(win, w=850, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')


# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý cà phê")
center_window(root)
root.resizable(False, False)

tk.Label(root, text="QUẢN LÝ CÀ PHÊ", font=("Arial", 20, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(fill="x", padx=10)

# ====== Tải dữ liệu bảng phụ ======
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


# ====== INPUT ======
tk.Label(frame, text="Mã cà phê").grid(row=0, column=0, sticky="w")
entry_ma = tk.Entry(frame, width=15)
entry_ma.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Tên cà phê").grid(row=0, column=2, sticky="w")
entry_ten = tk.Entry(frame, width=25)
entry_ten.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame, text="Loại").grid(row=1, column=0, sticky="w")
cbb_loai = ttk.Combobox(frame, width=25, state="readonly")
cbb_loai.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Giá").grid(row=1, column=2, sticky="w")
entry_gia = tk.Entry(frame, width=15)
entry_gia.grid(row=1, column=3, padx=5, pady=5)

tk.Label(frame, text="Số lượng").grid(row=2, column=0, sticky="w")
entry_sl = tk.Entry(frame, width=15)
entry_sl.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Ngày nhập").grid(row=2, column=2, sticky="w")
date_entry = DateEntry(frame, width=12, date_pattern="yyyy-mm-dd")
date_entry.grid(row=2, column=3, padx=5, pady=5)

tk.Label(frame, text="Nhà cung cấp").grid(row=3, column=0, sticky="w")
cbb_ncc = ttk.Combobox(frame, width=25, state="readonly")
cbb_ncc.grid(row=3, column=1, padx=5, pady=5)


# ====== Nạp combobox ======
def load_combobox():
    # Loại cà phê
    loai = load_loai()
    cbb_loai["values"] = [f"{a} - {b}" for a, b in loai]

    # Nhà cung cấp
    ncc = load_ncc()
    cbb_ncc["values"] = [f"{a} - {b}" for a, b in ncc]


load_combobox()


# ====== BẢNG ======
columns = ("ma", "ten", "tenloai", "gia", "soluong", "ngaynhap", "ncc")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

titles = ["Mã", "Tên", "Loại", "Giá", "SL", "Ngày", "Nhà CC"]
widths = [80, 150, 120, 80, 60, 100, 150]

for col, tit, w in zip(columns, titles, widths):
    tree.heading(col, text=tit)
    tree.column(col, width=w)

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


# ====== LOAD DỮ LIỆU ======
def load_data():
    for i in tree.get_children():
        tree.delete(i)

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.macaphe, c.tencaphe, l.tenloai, c.gia,
               c.soluong, c.ngaynhap, n.tenncc
        FROM caphe c
        LEFT JOIN loaicaphe l ON c.maloai = l.maloai
        LEFT JOIN nhacungcap n ON c.mancc = n.mancc
    """)

    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()


# ====== THÊM ======
def them():
    ma = entry_ma.get()
    ten = entry_ten.get()
    gia = entry_gia.get()
    sl = entry_sl.get()
    ngay = date_entry.get()

    # tách mã loại – tên loại
    maloai = cbb_loai.get().split(" - ")[0]
    mancc = cbb_ncc.get().split(" - ")[0]

    if ma == "" or ten == "":
        messagebox.showwarning("Thiếu dữ liệu", "Nhập mã và tên")
        return

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO caphe
            (macaphe, tencaphe, gia, soluong, ngaynhap, maloai, mancc)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (ma, ten, gia, sl, ngay, maloai, mancc))

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
        messagebox.showwarning("Chưa chọn", "Hãy chọn sản phẩm!")
        return

    ma = tree.item(sel)["values"][0]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM caphe WHERE macaphe=%s", (ma,))
    conn.commit()
    conn.close()

    load_data()


# ====== SỬA ======
def sua():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn", "Chọn 1 dòng để sửa")
        return

    values = tree.item(sel)["values"]

    entry_ma.delete(0, tk.END)
    entry_ma.insert(0, values[0])

    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, values[1])

    entry_gia.delete(0, tk.END)
    entry_gia.insert(0, values[3])

    entry_sl.delete(0, tk.END)
    entry_sl.insert(0, values[4])

    date_entry.set_date(values[5])


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

    cur.execute("""
        UPDATE caphe SET 
            tencaphe=%s, gia=%s, soluong=%s, ngaynhap=%s,
            maloai=%s, mancc=%s
        WHERE macaphe=%s
    """, (ten, gia, sl, ngay, maloai, mancc, ma))

    conn.commit()
    conn.close()

    load_data()
    clear_input()


# ====== BUTTON ======
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="Thêm", width=10, command=them).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Lưu", width=10, command=luu).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Sửa", width=10, command=sua).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Xóa", width=10, command=xoa).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Thoát", width=10, command=root.quit).grid(row=0, column=5, padx=5)

# LOAD
load_data()

root.mainloop()

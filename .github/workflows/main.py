import ctypes
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def write_iso(iso_path, drive):
    try:
        disk_path = fr"\\.\{drive}:"
        total = os.path.getsize(iso_path)
        done = 0
        with open(iso_path, "rb") as f_in, open(disk_path, "wb") as f_out:
            chunk = f_in.read(1024*1024)
            while chunk:
                f_out.write(chunk)
                done += len(chunk)
                chunk = f_in.read(1024*1024)
        messagebox.showinfo("完成", "ISO 写入成功！")
    except Exception as e:
        messagebox.showerror("错误", str(e))

def gui():
    root = tk.Tk()
    root.title("ISO 写盘工具 - 图形版")
    root.geometry("500x180")

    def browse():
        p = filedialog.askopenfilename(filetypes=[("ISO 文件", "*.iso")])
        if p:
            path_var.set(p)

    def start():
        iso = path_var.get().strip()
        drv = drive_var.get().strip().upper()
        if not iso or not drv:
            messagebox.showwarning("提示", "请填写完整")
            return
        write_iso(iso, drv)

    path_var = tk.StringVar()
    drive_var = tk.StringVar()

    tk.Label(root, text="ISO 文件：").place(x=20, y=20)
    tk.Entry(root, textvariable=path_var, width=40).place(x=100, y=20)
    tk.Button(root, text="浏览", command=browse).place(x=400, y=18)

    tk.Label(root, text="U盘盘符：").place(x=20, y=60)
    tk.Entry(root, textvariable=drive_var, width=10).place(x=100, y=60)

    tk.Button(root, text="开始写入", bg="#ff4444", fg="white",
              command=start, width=20).place(x=160, y=110)

    root.mainloop()

if __name__ == "__main__":
    run_as_admin()
    gui()

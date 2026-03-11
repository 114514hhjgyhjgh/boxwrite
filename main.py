import os
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox

def is_admin():
    """检查是否为管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def write_iso_to_drive(iso_path, drive_letter):
    """核心写盘逻辑"""
    try:
        # 物理磁盘路径
        drive_path = r'\\.\%s:' % drive_letter
        with open(iso_path, 'rb') as f_in:
            with open(drive_path, 'wb') as f_out:
                print(f"开始写入 {iso_path} 到 {drive_path}...")
                data = f_in.read(1024*1024) # 1MB 缓冲
                while data:
                    f_out.write(data)
                    data = f_in.read(1024*1024)
        return True
    except Exception as e:
        messagebox.showerror("写入失败", f"错误详情：\n{str(e)}")
        return False

def select_iso():
    """选择ISO文件"""
    path = filedialog.askopenfilename(filetypes=[("ISO Image Files", "*.iso;*.bin")])
    entry_iso.delete(0, tk.END)
    entry_iso.insert(0, path)

def start_write():
    """执行写入"""
    iso = entry_iso.get().strip()
    drive = entry_drive.get().strip().upper()
    
    if not iso or not drive:
        messagebox.showwarning("警告", "请选择ISO文件并输入U盘盘符！")
        return
        
    if messagebox.askyesno("确认", f"即将写入：\nISO: {iso}\nU盘: {drive}:\n\n请注意：这会清空U盘所有数据！是否继续？"):
        if write_iso_to_drive(iso, drive):
            messagebox.showinfo("成功", "ISO写入U盘完成！")

# --- GUI 界面 ---
if not is_admin():
    # 自动请求管理员权限
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

root = tk.Tk()
root.title("boxwrite 写盘工具")
root.geometry("450x180")

tk.Label(root, text="ISO 文件路径:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_iso = tk.Entry(root, width=30)
entry_iso.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="浏览", command=select_iso).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="U盘盘符 (如 G):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_drive = tk.Entry(root, width=10)
entry_drive.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Button(root, text="开始写入", command=start_write, bg="#ff4444", fg="white", padx=20, pady=5).grid(row=2, column=1, pady=20)

root.mainloop()

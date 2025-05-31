import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading

# اسم كرت الشبكة (يجب تعديله حسب جهازك)
ADAPTER_NAME = "Ethernet"

# --------------------- الدوال ---------------------

def change_ip():
    new_ip = entry_ip.get().strip()
    if not new_ip:
        messagebox.showwarning("تنبيه", "يرجى إدخال عنوان IP جديد.")
        return
    try:
        subprocess.run(
            f'wmic nicconfig where "Description like \'%{ADAPTER_NAME}%\'" call EnableStatic("{new_ip}", "255.255.255.0")',
            shell=True, check=True
        )
        messagebox.showinfo("نجاح", f"✅ تم تغيير عنوان IP إلى: {new_ip}")
    except subprocess.CalledProcessError:
        messagebox.showerror("خطأ", "فشل في تغيير IP. تأكد من تشغيل البرنامج كمسؤول ومن صحة اسم كرت الشبكة.")

def reset_ip():
    try:
        subprocess.run(
            f'wmic nicconfig where "Description like \'%{ADAPTER_NAME}%\'" call EnableDHCP',
            shell=True, check=True
        )
        messagebox.showinfo("نجاح", "✅ تم تعيين IP تلقائيًا (DHCP).")
    except subprocess.CalledProcessError:
        messagebox.showerror("خطأ", "فشل في تعيين IP تلقائي. تأكد من تشغيل البرنامج كمسؤول ومن صحة اسم كرت الشبكة.")

def check_ips():
    ip_list = text_ips.get("1.0", tk.END).strip().split()
    timeout = timeout_entry.get().strip()

    if not ip_list:
        messagebox.showwarning("تنبيه", "يرجى إدخال قائمة عناوين IP.")
        return
    if not timeout.isdigit():
        messagebox.showwarning("تنبيه", "يرجى إدخال رقم صحيح لمهلة الاتصال.")
        return

    timeout_ms = str(int(timeout))
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "🔄 جاري الفحص...\n")

    def ping_ips():
        unreachable = []
        for ip in ip_list:
            try:
                result = subprocess.run(
                    ["ping", "-n", "1", "-w", timeout_ms, ip],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if "TTL=" not in result.stdout:
                    unreachable.append(ip)
            except:
                unreachable.append(ip)

        result_text.delete("1.0", tk.END)
        if unreachable:
            result_text.insert(tk.END, "🔴 العناوين غير المتصلة:\n")
            for ip in unreachable:
                result_text.insert(tk.END, f"{ip}\n")
        else:
            result_text.insert(tk.END, "✅ كل العناوين متصلة.")

    threading.Thread(target=ping_ips).start()

# --------------------- واجهة المستخدم ---------------------

root = tk.Tk()
root.title("أداة إدارة عناوين IP")
root.geometry("600x650")
root.configure(bg="#f0f0f0")
root.resizable(False, False)

# ---------- العنوان الرئيسي ----------
title = tk.Label(root, text="🔧 أداة إدارة عناوين IP", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
title.pack(pady=10)

# ---------- إطار تغيير IP ----------
frame_ip = tk.LabelFrame(root, text="🛠️ تغيير عنوان IP", padx=10, pady=10, bg="#ffffff", font=("Arial", 12, "bold"))
frame_ip.pack(padx=15, pady=10, fill="x")

entry_ip = tk.Entry(frame_ip, font=("Arial", 12), width=30)
entry_ip.pack(pady=5)

btn_frame = tk.Frame(frame_ip, bg="#ffffff")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="تغيير IP", command=change_ip, bg="#4CAF50", fg="white", font=("Arial", 12), width=18).pack(side="left", padx=5)
tk.Button(btn_frame, text="تعيين تلقائي (DHCP)", command=reset_ip, bg="#FF9800", fg="white", font=("Arial", 12), width=18).pack(side="left", padx=5)

# ---------- إطار فحص IP ----------
frame_check = tk.LabelFrame(root, text="📡 فحص الاتصال", padx=10, pady=10, bg="#ffffff", font=("Arial", 12, "bold"))
frame_check.pack(padx=15, pady=10, fill="both", expand=False)

tk.Label(frame_check, text="أدخل عناوين IP (افصلها بمسافة):", font=("Arial", 12), bg="#ffffff").pack(anchor="w")
text_ips = scrolledtext.ScrolledText(frame_check, height=4, font=("Arial", 12))
text_ips.pack(pady=5, fill="x")

frame_timeout = tk.Frame(frame_check, bg="#ffffff")
frame_timeout.pack(pady=5)

tk.Label(frame_timeout, text="⏱️ المهلة (ms):", font=("Arial", 12), bg="#ffffff").pack(side="left")
timeout_entry = tk.Entry(frame_timeout, font=("Arial", 12), width=10)
timeout_entry.insert(0, "1000")
timeout_entry.pack(side="left", padx=5)

tk.Button(frame_check, text="🔍 بدء الفحص", command=check_ips, bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(pady=10)

# ---------- نتائج الفحص ----------
frame_result = tk.LabelFrame(root, text="📋 النتائج", padx=10, pady=10, bg="#ffffff", font=("Arial", 12, "bold"))
frame_result.pack(padx=15, pady=10, fill="both", expand=True)

result_text = scrolledtext.ScrolledText(frame_result, height=10, font=("Arial", 12), fg="red")
result_text.pack(fill="both", expand=True)

root.mainloop()

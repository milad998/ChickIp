import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading

# اسم كرت الشبكة (قم بتعديله حسب جهازك)
ADAPTER_NAME = "Ethernet"

# تغيير IP باستخدام wmic
def change_ip():
    new_ip = entry_ip.get().strip()
    if not new_ip:
        messagebox.showwarning("تنبيه", "يرجى إدخال عنوان IP جديد.")
        return

    try:
        subprocess.run(f'wmic nicconfig where "Description like \'%{ADAPTER_NAME}%\'" call EnableStatic("{new_ip}", "255.255.255.0")', shell=True, check=True)
        messagebox.showinfo("نجاح", f"✅ تم تغيير عنوان IP إلى: {new_ip}")
    except subprocess.CalledProcessError:
        messagebox.showerror("خطأ", "فشل في تغيير IP. تأكد من تشغيل البرنامج كمسؤول ومن صحة اسم كرت الشبكة.")

# إعادة IP إلى الوضع التلقائي (DHCP)
def reset_ip():
    try:
        subprocess.run(f'wmic nicconfig where "Description like \'%{ADAPTER_NAME}%\'" call EnableDHCP', shell=True, check=True)
        messagebox.showinfo("نجاح", "✅ تم تعيين IP تلقائيًا (DHCP).")
    except subprocess.CalledProcessError:
        messagebox.showerror("خطأ", "فشل في تعيين IP تلقائي. تأكد من تشغيل البرنامج كمسؤول ومن صحة اسم كرت الشبكة.")

# فحص قائمة IPs باستخدام ping
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
                result = subprocess.run(["ping", "-n", "1", "-w", timeout_ms, ip],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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

# --------------------- واجهة البرنامج ---------------------
root = tk.Tk()
root.title("أداة إدارة عناوين IP")
root.geometry("550x600")
root.resizable(False, False)

# ---------- تغيير IP ----------
tk.Label(root, text="🛠️ تغيير عنوان IP", font=("Arial", 14, "bold")).pack(pady=5)
entry_ip = tk.Entry(root, font=("Arial", 12), width=30)
entry_ip.pack(pady=5)

tk.Button(root, text="تغيير IP", command=change_ip, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=3)
tk.Button(root, text="إعادة إلى تلقائي (DHCP)", command=reset_ip, bg="#FF9800", fg="white", font=("Arial", 12)).pack(pady=5)

# ---------- فحص قائمة IPs ----------
tk.Label(root, text="📡 قائمة IPs للفحص (افصلها بمسافة):", font=("Arial", 12)).pack(pady=10)
text_ips = scrolledtext.ScrolledText(root, height=4, font=("Arial", 12))
text_ips.pack(padx=10)

# ---------- مهلة ping ----------
frame_ping = tk.Frame(root)
frame_ping.pack(pady=5)
tk.Label(frame_ping, text="⏱️ مهلة الاتصال (ms):", font=("Arial", 12)).pack(side="left")
timeout_entry = tk.Entry(frame_ping, font=("Arial", 12), width=10)
timeout_entry.insert(0, "1000")  # القيمة الافتراضية
timeout_entry.pack(side="left", padx=5)

# ---------- زر الفحص ----------
tk.Button(root, text="🔍 فحص الاتصال", command=check_ips, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

# ---------- النتائج ----------
tk.Label(root, text="📋 النتائج:", font=("Arial", 12)).pack()
result_text = scrolledtext.ScrolledText(root, height=10, font=("Arial", 12), fg="red")
result_text.pack(padx=10, pady=5, fill="both", expand=True)

root.mainloop()

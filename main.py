import tkinter as tk


MASTER_PASSWORD = "1234"             # sabit (constant)

# --Fonksiyonlar--
def on_login():             # giriş butonuna basıldığında çalışır
    password = password_entry.get()

    if password == "":
        message_label.config(text="Password cannot be empty", fg="red")

    elif password == MASTER_PASSWORD:
        open_notes_screen()              # 2. ekran fonkisoynu
        message_label.config(text="Login successful!", fg="green")
    else:
        message_label.config(text="wrong password", fg="red")


def open_notes_screen():
    login_frame.pack_forget()                  # giriş ekranını gizle
    notes_frame.pack(fill="both", expand=True)     # 2. ekranı aktif hale getirir



# GUI (Graphical User Interface) / Arayüz

root = tk.Tk()                 # ana pencere
root.title("Secret Notes")
root.geometry("600x400")

# Giriş ekranı (login frame)
login_frame = tk.Frame(root)                   # frame : ekran, bölüm.
login_frame.pack(fill="both", expand=True)      # Yatay + dikey doldur   # Boş alanı kapla

title_label = tk.Label(login_frame, text="Enter master password")
title_label.pack(pady=10)           # widget'i yerleştir     # üstten ve alttan boşluk

password_entry = tk.Entry(login_frame, show="*")       # yazılan karakteri yıldız yapar
password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=on_login)
login_button.pack(pady=10)

message_label = tk.Label(login_frame, text="")     # Boş yazı alanı, hata ya da başarı mesajı için
message_label.pack()

# Notlar bölümü Ekranı (Notes frame)
notes_frame = tk.Frame(root)
notes_label = tk.Label(notes_frame, text="Your secret notes")
notes_label.pack(pady=40)




















root.mainloop()
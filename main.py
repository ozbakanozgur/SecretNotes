import tkinter as tk
from tkinter import messagebox       # mesaj kutusu için (popup)
from cryptography.fernet import Fernet  # Şifreleme kütüphanesi
import os                         # dosya kontrolü için
import hashlib                    # Şifrelemeyi hashleme için

FONT = ("Helvetica", 12, "bold")
BG_COLOR = "gray64"


# -- Şifreleme Anahtarı İşlemleri --
def load_key():       # Şifre anahtarını dosyaya yükle veya yoksa oluştur
    try:
        with open("secret.key", "rb") as key_file:   # Mevcut anahtarı oku (rb: read binary)
            key = key_file.read()
    except FileNotFoundError:                       # anahtar yoksa oluştur
        key = Fernet.generate_key()             # 256 bit güvenli rastgele anahtar oluştur
        with open("secret.key", "wb") as key_file:   # anahtarı dosyaya yaz (wb: write binary)
            key_file.write(key)
    return key       # Anahtarı kullanmak üzere döndür

key = load_key()         # Yukarıdaki fonksiyonu çağırarak anahtarı hafızaya al
cipher = Fernet(key)         # Bu anahtarı kullanan bir şifreleme aracı (cipher) oluştur

# -- Şifre Dosyası Kontrolü --
def check_password_file():
    return os.path.exists("my_password.txt")   # Dosya varsa True, yoksa False döner

# -- Giriş ve Kayıt Fonksiyonu --
def on_action():             # giriş butonuna basıldığında çalışır
    password = password_entry.get()

    if password == "":
        message_label.config(text="Password cannot be empty", fg="dark red", font=FONT, bg=BG_COLOR )
        return

    # Durum 1: Eğer şifre dosyası varsa -> Giriş yapma modu
    if check_password_file():
        with open("my_password.txt", "r") as file:     # kayıtlı şifreyi oku
            saved_password = file.read().strip()      # .strip() boşlukları temizler

        # Girilen şifreyi hashle
        # .encode(): Yazıyı byte'a çevirir (hashlib byte ister)
        # .hexdigest(): Çıkan karmaşık byte'ları okunabilir yazıya çevirir
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # girilen şifre ile kayıtlı şifreyi karşılaştır
        if hashed_password == saved_password:
            open_notes_screen()              # Şifre doğruysa notları aç
            message_label.config(text="Login successful!", fg="green", font=FONT, bg=BG_COLOR)
        else:
            message_label.config(text="Wrong password", fg="dark red", font=FONT, bg=BG_COLOR)

    # Durum 2: Eğer şifre dosyası yoksa -> Kayıt modu
    else:
        # Girilen şifreyi hashleyip dosyaya kaydet
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with open("my_password.txt", "w") as file:
            file.write(hashed_password)


        message_label.config(text="Password set successfully! Please login", fg="green", font=FONT, bg=BG_COLOR)

        # Arayüzü giriş moduna çevir
        title_label.config(text="Enter your password to login", font=FONT, bg=BG_COLOR)
        action_button.config(text="Login")
        password_entry.delete(0, tk.END)   # Kutuyu temizle

def open_notes_screen():
    login_frame.pack_forget()                  # giriş ekranını gizle
    notes_frame.pack(fill="both", expand=True)     # 2. ekranı aktif hale getirir

    # Ekran açıldığında eski notları yükle ve şifresini çöz
    try:
        with open("notes.txt", "rb") as file:     # Dosyayı binary okuma modunda ("rb") aç
            encrypted_notes = file.read()            # şifreli içeriği oku

            # .decrypt(): Şifreli veriyi orjinal haline çevirir
            # .decode(): Byte verisini tekrar yazıya (string) çevirir
            decrypted_notes = cipher.decrypt(encrypted_notes).decode() # şifresini çöz
            notes_text.insert(tk.END, decrypted_notes)   # metin kutusuna ekle
    except FileNotFoundError:
        pass    # Dosya henüz yoksa (ilk kez açılıyorsa) hiçbir şey yapma
    except Exception:
        # Şifre çözülemezse veya dosya boşsa
        pass



def save_notes():
    notes = notes_text.get("1.0", tk.END).strip()    # Tüm metni al ve boşlukları sil

    if not notes:  # not boşsa kaydetme
        return

    # Notları şifrele (Encryption)
    # .encode(): Yazıyı byte'a çevirir (şifreleme byte ile çalışır)
    # .encrypt(): Veriyi okunamaz hale getirir
    encrypted_notes = cipher.encrypt(notes.encode())

    # Dosya işlemleri
    try:
        with open("notes.txt", "wb") as file:   # Doyayayı binary yazma modunda aç ("wb")
            file.write(encrypted_notes)            # şifreli Notları dosyaya yaz
            messagebox.showinfo("Success", "Notes saved and encrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save notes: {e}")  # hata olursa bildir

# -- GUI (Arayüz) Tasarımı --

root = tk.Tk()                 # ana pencere
root.title("Secret Notes")
root.geometry("600x400")

# 1-Giriş ekranı (login frame)
login_frame = tk.Frame(root, bg=BG_COLOR)                   # frame : ekran, bölüm.
login_frame.pack(fill="both", expand=True)      # Yatay + dikey doldur   # Boş alanı kapla


# Başlangıç metnini duruma göre ayarla
# Eğer şifre dosyası varsa "Giriş Yap", yoksa "Şifre Belirle" yazsın
if check_password_file():
    start_text = "Enter your password"
    button_text = "Login"
else:
    start_text = "Set your master password"
    button_text = "Set Password"


title_label = tk.Label(login_frame, text=start_text, font=FONT, bg=BG_COLOR)
title_label.pack(pady=10)           # widget'i yerleştir     # üstten ve alttan boşluk

password_entry = tk.Entry(login_frame, show="*", font=FONT)       # yazılan karakteri yıldız yapar
password_entry.pack()

action_button = tk.Button(login_frame, text=button_text, command=on_action, font=FONT)
action_button.pack(pady=10)

message_label = tk.Label(login_frame, text="", bg=BG_COLOR)     # Boş yazı alanı, hata ya da başarı mesajı için
message_label.pack()

# 2-Notlar bölümü Ekranı (Notes frame)
notes_frame = tk.Frame(root, bg=BG_COLOR)

notes_label = tk.Label(notes_frame, text="Your notes", font=FONT, bg=BG_COLOR)
notes_label.pack(pady=10)

# Not yazma alanı (Text widget)
notes_text = tk.Text(notes_frame, height=10, width=40, font=FONT)
notes_text.pack(pady=10)

# Kaydet butonu
save_button = tk.Button(notes_frame, text="Save Notes", command=save_notes, font=FONT)
save_button.pack(pady=10)

















root.mainloop()
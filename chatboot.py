import tkinter as tk
from tkinter import scrolledtext
from groq import Groq

# ==========================================
# 1. KONFIGURASI API GROQ
# ==========================================
# Masukkan API Key dari Groq Console kamu di sini
GROQ_API_KEY = "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"

# Inisialisasi Klien Groq
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Gagal inisialisasi API Groq: {e}")

# ... (kode impor library dan API_KEY di atasnya tetap sama) ...

def dapatkan_jawaban_ai(pesan_user):
    # <<< GANTI BAGIAN INI DENGAN YANG BARU >>>
    instruksi_peran = (
        "Kamu adalah InfoBot, seorang asisten guru Informatika yang ramah, interaktif, dan sangat pintar. "
        "Tugasmu adalah menjawab pertanyaan pengguna seputar Informatika / Ilmu Komputer dengan jelas. "
        "Selalu gunakan analogi sehari-hari jika menjelaskan konsep yang rumit. "
        "Gunakan Bahasa Indonesia yang santai, suportif, tapi tetap sopan.\n\n"
        "ATURAN FORMAT JAWABAN:\n"
        "1. JANGAN gunakan format Markdown seperti bintang-bintang (**teks**), pagar (###), atau garis miring.\n"
        "2. Gunakan huruf kapital biasa untuk penekanan kata penting.\n"
        "3. Berikan jarak/spasi kosong (line break) yang cukup antar paragraf agar enak dibaca.\n"
        "4. Jika memberikan contoh kode program, buat pembatas yang jelas dengan garis baru, tidak perlu menggunakan simbol backtick (```)."
    )
    
    try:
        
# ... (sisa kode ke bawahnya tetap sama semua) ...
        # Menggunakan model 'llama-3.3-70b-versatile' yang sangat pintar dan gratis di Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": instruksi_peran
                },
                {
                    "role": "user",
                    "content": pesan_user
                }
            ],
            model="llama-3.3-70b-versatile", # Model Llama 3.3 yang cerdas dan cepat
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Jika model 70b sedang padat, kita gunakan fallback model Llama 3.1 8B yang super cepat
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instruksi_peran},
                    {"role": "user", "content": pesan_user}
                ],
                model="llama-3.1-8b-instant",
            )
            return chat_completion.choices[0].message.content
        except Exception as err_fallback:
            return f"Waduh, koneksi ke Groq terputus nih. Error: {err_fallback}"

# ==========================================
# 2. ANTARMUKA APLIKASI (GUI TKINTER)
# ==========================================
def kirim_pesan():
    pesan_user = input_user.get()
    if pesan_user.strip() == "":
        return
        
    # Tampilkan chat dari User ke layar
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "Kamu: " + pesan_user + "\n\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)
    
    # Kosongkan kolom input setelah kirim
    input_user.delete(0, tk.END)
    
    # Jalankan proses pemanggilan AI di latar belakang (agar aplikasi tidak membeku)
    root.after(100, lambda: proses_jawaban_bot(pesan_user))

def proses_jawaban_bot(pesan_user):
    # Memanggil fungsi AI untuk mendapatkan jawaban
    jawaban_bot = dapatkan_jawaban_ai(pesan_user)
    
    # Tampilkan chat jawaban dari InfoBot ke layar
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "InfoBot:\n" + jawaban_bot + "\n\n" + "—" * 40 + "\n\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# Inisialisasi Window Utama
root = tk.Tk()
root.title("InfoBot AI (Groq) - Asisten Informatika")
root.geometry("500x650")
root.configure(bg="#f4f6f9")

# Judul Header Aplikasi
header_label = tk.Label(
    root, 
    text="💻 Chatboot  Asisten Belajar Informatika (By Musa)", 
    font=("Helvetica", 12, "bold"), 
    bg="#17A2B8", # Warna teal cerah khas Groq
    fg="white", 
    pady=10
)
header_label.pack(fill=tk.X)

# Area Tampilan Chat (Scrollable)
chat_window = scrolledtext.ScrolledText(
    root, 
    wrap=tk.WORD, 
    state=tk.DISABLED, 
    bg="#ffffff", 
    font=("Segoe UI", 10),
    padx=10,
    pady=10
)
chat_window.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

# Memasukkan Pesan Sambutan Pertama Kali
chat_window.config(state=tk.NORMAL)
chat_window.insert(
    tk.END, 
    "Assalamu'alaikum, Gimana kabarnya, aku berharap Anda semua dalam keadaan sehat ya"
    "Saya lagi belajar membuat Chatboot sederhana dan berharap ada manfaatnya untuk kita seua\n"
    "Mau mulai belajar atau diskusi soal apa hari ini?\n\n" + "—" * 30 + "\n\n"
)
chat_window.config(state=tk.DISABLED)

# Frame Bagian Bawah (Input & Tombol)
bottom_frame = tk.Frame(root, bg="#f4f6f9")
bottom_frame.pack(padx=15, pady=10, fill=tk.X)

# Kolom Tempat Mengetik Pesan
input_user = tk.Entry(
    bottom_frame, 
    font=("Segoe UI", 11), 
    bg="#ffffff", 
    relief=tk.SOLID, 
    bd=1
)
input_user.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
input_user.bind("<Return>", lambda event: kirim_pesan()) # Kirim saat tekan Enter

# Tombol Kirim Chat
tombol_kirim = tk.Button(
    bottom_frame, 
    text="Kirim Pesan", 
    command=kirim_pesan, 
    bg="#17A2B8", 
    fg="white", 
    font=("Segoe UI", 10, "bold"),
    relief=tk.FLAT,
    padx=15,
    pady=5
)
tombol_kirim.pack(side=tk.RIGHT)

# Menjalankan Aplikasi Utama
root.mainloop()

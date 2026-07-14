import streamlit as st
from groq import Groq

# ==========================================
# 1. KONFIGURASI HALAMAN WEB STREAMLIT
# ==========================================
st.set_page_config(
    page_title="InfoBot AI - Asisten Informatika", 
    page_icon="💻", 
    layout="centered"
)

# Judul Header Aplikasi (Menggantikan tk.Label)
st.title("💻 Chatboot Asisten Belajar Informatika (By Musa)")
st.write("Tanyakan apa saja seputar materi Informatika, pemrograman, atau logika komputer!")
st.markdown("---")

# ==========================================
# 2. KONFIGURASI & INTEGRASI API GROQ
# ==========================================
# Membaca API Key dengan aman (Otomatis beralih antara server Streamlit Cloud / Lokal)
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # Isikan API Key kamu di sini jika dijalankan secara lokal di komputer sendiri
    GROQ_API_KEY = "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"

# Inisialisasi Klien Groq
if "groq_client" not in st.session_state:
    try:
        st.session_state.groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.error(f"Gagal inisialisasi API Groq: {e}")

def dapatkan_jawaban_ai(pesan_user):
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
        # Menggunakan model 'llama-3.3-70b-versatile'
        chat_completion = st.session_state.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruksi_peran},
                {"role": "user", "content": pesan_user}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Fallback model jika server utama sibuk
        try:
            chat_completion = st.session_state.groq_client.chat.completions.create(
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
# 3. MANAJEMEN RIWAYAT CHAT (Session State)
# ==========================================
# Menggantikan fungsi chat_window Tkinter agar riwayat pesan tidak hilang saat web dimuat ulang
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": (
                "Assalamu'alaikum, Gimana kabarnya, aku berharap Anda semua dalam keadaan sehat ya. "
                "Saya lagi belajar membuat Chatboot sederhana dan berharap ada manfaatnya untuk kita semua.\n\n"
                "Mau mulai belajar atau diskusi soal apa hari ini?"
            )
        }
    ]

# Tampilkan seluruh chat yang ada di memori riwayat ke layar web
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# 4. ANTARMUKA INPUT USER (Menggantikan tk.Entry & Button)
# ==========================================
if prompt := st.chat_input("Ketik pesan di sini..."):
    # Tampilkan pesan ketikan user langsung ke layar web
    with st.chat_message("user"):
        st.write(prompt)
    
    # Simpan pesan user ke memori riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Tampilkan animasi loading saat bot sedang berpikir
    with st.chat_message("assistant"):
        placeholder = st.empty()
        # Ambil jawaban dari AI
        jawaban_bot = dapatkan_jawaban_ai(prompt)
        # Tampilkan jawaban di layar web
        placeholder.write(jawaban_bot)
        
    # Simpan jawaban bot ke memori riwayat
    st.session_state.messages.append({"role": "assistant", "content": jawaban_bot})

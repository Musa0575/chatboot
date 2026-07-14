import streamlit as st
from groq import Groq
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA (CSS)
# ==========================================
st.set_page_config(
    page_title="InfoBot - Guru Informatika", 
    page_icon="💻", 
    layout="centered"
)

# Menambahkan CSS Kustom agar tampilan Chat lebih cantik dan modern
st.markdown("""
    <style>
    /* Mengubah font dan background aplikasi */
    .stApp {
        background-color: #f7f9fc;
    }
    /* Mendesain judul utama */
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #17A2B8;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    /* Mendesain sub-judul */
    .sub-title {
        text-align: center;
        color: #5a626a;
        font-size: 14px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MENU SIDEBAR (SAMPING) - AGAR LEBIH RAPI
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80) # Icon Robot Lucu
    st.markdown("### 🤖 Tentang InfoBot")
    st.info(
        "Aplikasi ini dibuat oleh **Musa** sebagai proyek belajar pemrograman "
        "dan kecerdasan buatan (AI). Semoga bermanfaat untuk belajar Informatika!"
    )
    
    st.markdown("---")
    st.markdown("### 💡 Topik yang Bisa Ditanyakan:")
    st.caption("• Apa itu Array dan hubungannya dengan laci lemari?")
    st.caption("• Bagaimana cara kerja internet mampir ke rumah kita?")
    st.caption("• Buatkan kode Python untuk hitung nilai rata-anak.")
    
    st.markdown("---")
    # Tombol Reset Chat untuk menghapus riwayat obrolan
    if st.button("🔄 Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 3. HEADER UTAMA (TAMPILAN TENGAH)
# ==========================================
st.markdown('<h1 class="main-title">💻 InfoBot AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Asisten Belajar Informatika Interaktif • By Musa</p>', unsafe_allow_html=True)

# ==========================================
# 4. INTEGRASI API GROQ
# ==========================================
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = "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"

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
        "1. JANGAN gunakan format Markdown kasar seperti pagar (###). Gunakan poin-poin tebal biasa.\n"
        "2. Gunakan spasi kosong (line break) yang cukup antar paragraf agar nyaman dibaca di layar HP.\n"
        "3. Jika memberikan contoh kode program, buat pembatas kode yang bersih."
    )
    
    try:
        chat_completion = st.session_state.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruksi_peran},
                {"role": "user", "content": pesan_user}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
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
# 5. RIWAYAT CHAT & EFEK MENGETIK
# ==========================================
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": (
                "Assalamu'alaikum! Bagaimana kabarnya? Saya berharap Anda semua dalam keadaan sehat ya. 😊\n\n"
                "Saya InfoBot, asisten Informatika yang dibuat oleh Musa. Kita bisa berdiskusi tentang "
                "coding, hardware, jaringan, atau logika komputer.\n\n"
                "Mau mulai belajar atau diskusi soal apa hari ini?"
            )
        }
    ]

# Tampilkan pesan dari memori
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input pesan baru
if prompt := st.chat_input("Ketik pertanyaan Informatika kamu di sini..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        jawaban_full = dapatkan_jawaban_ai(prompt)
        
        # --- TRIK EFEK MENGETIK (STREAMING TEXT EFFECT) ---
        # Membuat teks muncul kata demi kata agar tampak hidup
        jawaban_animasi = ""
        for kata in jawaban_full.split(" "):
            jawaban_animasi += kata + " "
            time.sleep(0.04) # Mengatur kecepatan ketikan
            placeholder.write(jawaban_animasi + "▌")
        placeholder.write(jawaban_full) # Tampilkan utuh tanpa kursor ketik di akhir
        
    st.session_state.messages.append({"role": "assistant", "content": jawaban_full})

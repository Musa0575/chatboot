import streamlit as st
from groq import Groq
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA
# ==========================================
st.set_page_config(
    page_title="Portal & AI - Yayasan Pendidikan", 
    page_icon="🏫", 
    layout="centered"
)

# Custom CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .title-portal { color: #17A2B8; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .subtitle-portal { text-align: center; color: #6c757d; font-size: 14px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# Header Utama Aplikasi
st.markdown('<h1 class="title-portal">🏫 Portal Informasi & AI Sekolah</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-portal">Sistem Informasi Akademik Terpadu • Dikembangkan oleh Musa</p>', unsafe_allow_html=True)

# ==========================================
# 2. MEMBUAT MENU TAB (NAVIGASI)
# ==========================================
# Di sini kita membuat 3 menu utama yang bisa diklik pengguna
tab1, tab2, tab3 = st.tabs(["📜 Profil Yayasan", "📅 Jadwal & Akademik", "🤖 Tanya InfoBot AI"])

# ------------------------------------------
# MENU 1: PROFIL YAYASAN
# ------------------------------------------
with tab1:
    st.subheader("🏛️ Profil Yayasan Pendidikan")
    st.write(
        "Selamat datang di Portal Resmi Yayasan. Kami berkomitmen untuk menyelenggarakan "
        "pendidikan yang berintegritas, memanfaatkan teknologi modern, dan berkarakter mulia."
    )
    
    # Menggunakan kolumnar agar tampilan informasi rapi sejajar
    col1, col2 = st.columns(2)
    with col1:
        st.info("🎯 **Visi Kami**\n\nMenjadi lembaga pendidikan unggulan yang melahirkan generasi cerdas teknologi dan berakhlak karimah.")
    with col2:
        st.success("🚀 **Misi Kami**\n\n1. Menyelenggarakan pembelajaran Informatika berbasis praktik.\n2. Membangun kreativitas siswa melalui inovasi digital.")

# ------------------------------------------
# MENU 2: JADWAL SEKOLAH & PELAJARAN
# ------------------------------------------
with tab2:
    st.subheader("📅 Jadwal Pelajaran & Kegiatan Sekolah")
    
    # Membuat pilihan kelas menggunakan selectbox
    pilihan_kelas = st.selectbox("Pilih Kelas untuk Melihat Jadwal:", ["Kelas 10 - Informatika", "Kelas 11 - Rekayasa Perangkat Lunak"])
    
    if pilihan_kelas == "Kelas 10 - Informatika":
        # Membuat tabel jadwal menggunakan dictionary data Streamlit
        jadwal_k10 = {
            "Hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
            "07.30 - 09.00": ["Upacara & Agama", "Matematika", "Bahasa Indonesia", "Dasar Informatika", "Olah Raga"],
            "09.30 - 11.30": ["Bahasa Inggris", "Fisika", "Pemrograman Python", "Jaringan Komputer", "Pengembangan Diri"]
        }
        st.table(jadwal_k10) # Menampilkan tabel yang rapi otomatis
    
    elif pilihan_kelas == "Kelas 11 - Rekayasa Perangkat Lunak":
        jadwal_k11 = {
            "Hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
            "07.30 - 09.00": ["Basis Data", "Matematika Diskrit", "Pendidikan Pancasila", "Pemrograman Web", "Bimbingan Konseling"],
            "09.30 - 11.30": ["Bahasa Inggris", "Struktur Data", "Cloud Computing", "Kewirausahaan", "Kerja Praktik"]
        }
        st.table(jadwal_k11)
        
    st.markdown("---")
    st.subheader("🔔 Pengumuman Penting Pekan Ini")
    st.warning("📅 **15 Juli 2026** - Batas akhir pengumpulan proyek pembuatan Chatbot kelompok.")

# ------------------------------------------
# MENU 3: CHATBOT AI (KODE LAMA KAMU)
# ------------------------------------------
with tab3:
    st.subheader("🤖 Ngobrol dengan InfoBot AI")
    st.caption("Butuh bantuan belajar? Tanyakan langsung pada bot pintar di bawah ini!")

    # Integrasi API Groq (Tetap aman menggunakan Secrets)
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
            "Kamu adalah InfoBot, seorang asisten guru Informatika yang ramah dan pintar. "
            "Tugasmu membantu menjawab pertanyaan seputar ilmu komputer."
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
            return f"Maaf, koneksi server AI sedang padat. Silakan coba lagi. (Error: {e})"

    # Inisialisasi Memori Chat khusus di Tab 3
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Assalamu'alaikum! Ada materi Informatika atau sekolah yang ingin kamu diskusikan hari ini? 😊"}
        ]

    # Menampilkan riwayat chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Logika Input Chat
    if prompt := st.chat_input("Ketik pesan kamu di sini..."):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            jawaban_bot = dapatkan_jawaban_ai(prompt)
            
            # Efek mengetik berjalan
            jawaban_animasi = ""
            for kata in jawaban_bot.split(" "):
                jawaban_animasi += kata + " "
                time.sleep(0.04)
                placeholder.write(jawaban_animasi + "▌")
            placeholder.write(jawaban_bot)
            
        st.session_state.messages.append({"role": "assistant", "content": jawaban_bot})

# ==========================================
# 3. SIDEBAR INFORMASI PENYALUR
# ==========================================
with st.sidebar:
    st.markdown("### 🏫 Menu Navigasi Samping")
    st.write("Gunakan tab di bagian tengah untuk melihat informasi lengkap lembaga.")
    st.markdown("---")
    st.caption("© 2026 Portal Sekolah - Dibuat dengan Python & Streamlit.")

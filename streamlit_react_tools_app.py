# streamlit_career_chatbot.py
import streamlit as st
import google.generativeai as genai
import os
import re
import html

# ---------------------------
# 1. KONFIGURASI HALAMAN & GAYA (CSS)
# ---------------------------
st.set_page_config(page_title="CerA - Career Pathfinder AI", page_icon="🎯", layout="wide")

# Custom CSS untuk tampilan yang lebih menarik
st.markdown(
    """
    <style>
    /* Latar belakang halaman */
    .stApp, .block-container {
        background: radial-gradient(circle at top left, #0b1220, #0f1724);
        color: #e6eef8;
        font-family: 'Inter', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    /* Header */
    .header {
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(9,11,20,0.6);
        text-align: center;
    }
    .header h1 { margin:0; color: #fff; letter-spacing: .6px; }
    .header p { margin:4px 0 0 0; color: rgba(255,255,255,0.9); }

    /* Kustomisasi input chat Streamlit */
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.03) !important;
        color: #e6eef8 !important;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    /* Mengubah warna teks placeholder */
    .stTextInput>div>div>input::placeholder {
        color: #7b88a1 !important;
    }

    /* Kartu Roadmap */
    .roadmap {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        padding: 16px;
        border-radius: 12px;
        margin-top: 12px;
    }
    .roadmap h4 { color: #cfe3ff; margin: 0 0 8px 0; }
    .roadmap li { margin: 6px 0; padding-left: 8px; }

    /* Footer fixed at very bottom */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(10, 10, 20, 0.95);
        text-align:center;
        font-size:13px;
        padding:10px 0;
        border-top:1px solid rgba(255,255,255,0.08);
        color:#aaa;
        z-index:9999;
    }
    .footer b { color:#fff; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tampilan Header
st.markdown(
    """
    <div class='header'>
        <h1>🤖 CerA : Career Pathfinder AI</h1>
        <p>Konselor karier virtual Anda. Ceritakan minat dan tujuan Anda, dan saya akan bantu menyusun langkah-langkahnya.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# 2. PENGATURAN SIDEBAR
# ---------------------------
with st.sidebar:
    st.header("⚙️ Pengaturan")
    tone = st.selectbox("Gaya Bahasa", ["Santai", "Formal", "Motivatif"])
    temperature = st.sidebar.slider("Tingkat Kreativitas", 0.0, 1.0, 0.4, 0.05)
    show_roadmap = st.sidebar.checkbox("Tampilkan ringkasan roadmap", value=True)
    st.sidebar.caption("Pastikan GEMINI_API_KEY sudah diatur di Secrets Streamlit.")
    
    # Tombol untuk mereset percakapan
    if st.button("🔄 Reset Percakapan", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---------------------------
# 3. INISIALISASI MODEL GEMINI
# ---------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
model = None

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.warning(f"⚠️ Gagal mengonfigurasi Gemini API: {e}", icon="🔑")
else:
    st.info("ℹ️ Kunci API Gemini tidak ditemukan. Aplikasi berjalan dalam mode demo.", icon="🤖")

# ---------------------------
# 4. MANAJEMEN SESSION STATE
# ---------------------------
# Inisialisasi riwayat pesan jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# 5. FUNGSI-FUNGSI BANTUAN (UTILITIES)
# ---------------------------
def escape_html(s: str) -> str:
    """Menghindari injeksi HTML pada output."""
    return html.escape(s)

KEYWORDS_ROADMAP = [r"\broadmap\b", r"\blangkah\b", r"\brencana\b", r"\bmulai dari mana\b", r"\bapa yang harus\b"]

def wants_roadmap(text: str) -> bool:
    """Mendeteksi apakah pengguna meminta roadmap."""
    t = text.lower()
    return any(re.search(p, t) for p in KEYWORDS_ROADMAP)

def call_gemini_api(prompt: str, temp: float) -> str:
    """Memanggil API Gemini dan mengembalikan respons teks."""
    if not model:
        # Fallback jika API tidak aktif
        if wants_roadmap(prompt):
            return (
                "Tentu, ini adalah roadmap umum yang bisa jadi panduan awal:\n"
                "1. **Fondasi:** Pelajari konsep dasar dari bidang yang kamu minati.\n"
                "2. **Peralatan (Tools):** Kuasai perangkat lunak atau tools yang umum digunakan di industri itu (misalnya: Python untuk data, Figma untuk desain).\n"
                "3. **Portofolio:** Buat 2-3 proyek nyata untuk menunjukkan kemampuanmu.\n"
                "4. **Jaringan (Networking):** Bergabung dengan komunitas online dan cari seorang mentor.\n"
                "5. **Aksi:** Mulai melamar untuk posisi magang atau entry-level untuk mendapatkan pengalaman pertama."
            )
        return "Mode demo: Halo! Ceritakan lebih detail tentang minatmu."
    
    try:
        # Mengirim prompt ke model Gemini
        response = model.generate_content(prompt, generation_config={"temperature": temp, "max_output_tokens": 1024})
        return response.text
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil API: {e}")
        return "Maaf, terjadi sedikit kendala. Bisa coba tanyakan lagi?"

def build_prompt() -> str:
    """Membangun prompt lengkap dengan instruksi sistem dan riwayat percakapan."""
    # Instruksi sistem untuk AI
    system_instruction = (
        "Kamu adalah 'CerA', seorang konselor karier AI yang ramah, suportif, dan cerdas. "
        "Tujuan utamamu adalah membantu pengguna menemukan jalur karier yang sesuai dengan minat mereka. "
        "Gunakan bahasa Indonesia yang natural dan mudah dipahami. "
        "Selalu berikan jawaban yang terstruktur, positif, dan dapat ditindaklanjuti. "
        f"Gunakan gaya bahasa: **{tone}**."
    )
    
    # Menggabungkan riwayat pesan menjadi satu string
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    
    # Mengembalikan prompt yang siap dikirim
    return f"{system_instruction}\n\n--- Riwayat Percakapan ---\n{history}\nassistant:"

# ---------------------------
# 6. TAMPILAN DAN LOGIKA CHAT
# ---------------------------
# Tampilkan riwayat pesan yang sudah ada
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Terima input dari pengguna
user_prompt = st.chat_input("Hai! Gimana kabarnya hari ini? Ceritain yuk, hal yang lagi kamu pikirin soal karier 💬")

if user_prompt:
    # Tambahkan pesan pengguna ke riwayat dan tampilkan
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Buat dan tampilkan respons dari asisten
    with st.chat_message("assistant"):
        with st.spinner("CerA sedang berpikir... 🤔"):
            # Bangun prompt lengkap
            full_prompt = build_prompt()
            # Panggil API
            assistant_response = call_gemini_api(full_prompt, temperature)
            st.markdown(assistant_response)
    
    # Tambahkan respons asisten ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Otomatis tampilkan kartu roadmap jika diminta
    if show_roadmap and wants_roadmap(user_prompt):
        steps = []
        # Ekstrak langkah-langkah dari jawaban bot
        for line in assistant_response.splitlines():
            line = line.strip()
            # Cari baris yang terlihat seperti item list (dimulai dengan angka, bintang, atau strip)
            if re.match(r"^(\d+\.|-|\*|\u2022)", line):
                # Bersihkan penanda list
                clean_line = re.sub(r'^[\d\.\-\*\u2022\s]+', '', line).strip()
                if clean_line:
                    steps.append(clean_line)
        
        if steps:
            st.markdown("<div class='roadmap'>", unsafe_allow_html=True)
            st.markdown("<h4>🛣️ Ringkasan Roadmap</h4>", unsafe_allow_html=True)
            # Buat daftar bernomor
            roadmap_html = "<ol>" + "".join(f"<li>{escape_html(s)}</li>" for s in steps) + "</ol>"
            st.markdown(roadmap_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# 7. FOOTER
# ---------------------------
st.markdown("""
<div class='footer'>
    Dibuat dengan ❤️ oleh <b>Career Pathfinder AI</b> — Berbasis Streamlit & Google Gemini API
</div>
""", unsafe_allow_html=True)
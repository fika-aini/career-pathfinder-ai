import streamlit as st
import google.generativeai as genai
from datetime import datetime

# -------------------------
# CONFIGURATION
# -------------------------
st.set_page_config(page_title="Career Pathfinder AI", page_icon="💼", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# -------------------------
# PERSONA PROMPT
# -------------------------
BASE_PROMPT = """
Kamu adalah Cera, AI Career Coach yang empatik dan cerdas.
Gunakan bahasa Indonesia santai namun sopan. Jika pengguna menggunakan istilah Inggris atau gaul, pahami konteksnya dan jawab dengan bahasa yang mudah dimengerti.
Peranmu adalah membantu pengguna memahami minat, kekuatan, dan arah karier yang sesuai.
Kamu bukan peramal pekerjaan, tapi konselor yang membantu refleksi diri dan memberikan saran praktis.
Setelah memberi rekomendasi karier, bantu pengguna dengan roadmap singkat: langkah belajar, keterampilan dasar, dan sumber daya yang disarankan.
"""

# -------------------------
# SESSION STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": BASE_PROMPT}]

# -------------------------
# SIDEBAR SETTINGS
# -------------------------
st.sidebar.title("⚙️ Pengaturan Chatbot")
style = st.sidebar.selectbox("Gaya Bahasa", ["Formal", "Santai", "Motivatif"])
temp = st.sidebar.slider("Kreativitas (Temperature)", 0.0, 1.0, 0.4)
st.sidebar.markdown("---")
st.sidebar.caption("Gunakan gaya bahasa sesuai preferensi percakapan.")

# -------------------------
# MAIN TITLE
# -------------------------
st.title("💼 Career Pathfinder AI")
st.caption("Temukan potensi dan arah kariermu bersama Cera – AI Career Coach.")

# -------------------------
# GEMINI MODEL
# -------------------------
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=st.session_state.messages)
    response = chat.send_message(prompt, generation_config=genai.types.GenerationConfig(
        temperature=temp
    ))
    return response.text

# -------------------------
# USER INPUT
# -------------------------
user_input = st.text_input("Ketik pertanyaan, cerita minat, atau kebingungan kariermu di sini...")

if st.button("Kirim"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Cera sedang memikirkan jawabannya..."):
            response = chat_with_gemini(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# -------------------------
# CHAT DISPLAY
# -------------------------
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(f"**Kamu:** {msg['content']}")
    else:
        st.chat_message("assistant").markdown(f"**Cera:** {msg['content']}")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("Dibangun menggunakan Streamlit & Google Gemini API | © 2025 Career Pathfinder AI")
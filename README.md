 # 💼 Career Pathfinder AI (CerA)

[![Built with Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Powered by Google Gemini](https://img.shields.io/badge/Powered_by-Google_Gemini-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)

> "Temukan arah kariermu dengan kekuatan AI—dipandu oleh empati, wawasan, dan data."

**Career Pathfinder AI** adalah chatbot cerdas yang dirancang untuk bertindak sebagai **AI Career Coach** pribadi Anda, bernama **Cera**. Cera membantu Anda memahami potensi, minat, dan arah karier yang paling sesuai, serta menyediakan **roadmap pembelajaran** yang praktis untuk memulai.

Aplikasi ini dibangun menggunakan **Streamlit** dan **Google Gemini API**, dengan fokus pada percakapan natural dalam Bahasa Indonesia yang relevan dengan generasi saat ini.

---

## 📸 Tampilan Aplikasi

| Tampilan Utama | 
| :---: |
| ![Tampilan Utama Aplikasi](https://raw.githubusercontent.com/fika-aini/career-pathfinder-ai/main/example_conversation.png) |

---

## ✨ Fitur Utama

* **🤖 Percakapan Kontekstual:** Didukung oleh Gemini API untuk dialog yang mengalir secara alami.
* **👤 Persona AI "Cera":** Dirancang untuk menjadi konselor karier yang ramah, empatik, dan suportif.
* **🎨 Gaya Bahasa Dinamis:** Sesuaikan gaya bicara Cera (Santai, Formal, atau Motivatif) melalui sidebar.
* **🎯 Rekomendasi Terpersonalisasi:** Dapatkan saran karier yang relevan berdasarkan minat dan cerita Anda.
* **🗺️ Generator Roadmap Karier:** Secara otomatis menghasilkan langkah-langkah belajar, skill dasar, dan sumber daya yang relevan.
* **🧠 Memori Percakapan:** Cera mengingat konteks percakapan untuk interaksi yang lebih mendalam.

---

## 🛠️ Tumpukan Teknologi (Tech Stack)

* **Framework Aplikasi:** [Streamlit](https://streamlit.io/)
* **Model AI:** [Google Gemini API](https://aistudio.google.com/)
* **Bahasa Pemrograman:** Python
* **Library Utama:** `streamlit`, `google-generativeai`

---

## 🚀 Panduan Memulai

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer lokal Anda.

### 1. Prasyarat

* Pastikan Anda sudah menginstal **Python 3.11** atau versi yang lebih baru.
* Memiliki akun Google dan **API Key** dari Google AI Studio.

### 2. Kloning dan Instalasi

```bash
# 1. Kloning repository ini
git clone [https://github.com/fika-aini/career-pathfinder-ai.git](https://github.com/fika-aini/career-pathfinder-ai.git)
cd career-pathfinder-ai

# 2. Instal semua dependensi yang dibutuhkan
pip install -r requirements.txt
```

### 3. Konfigurasi API Key

Buat file baru di dalam direktori proyek Anda: `.streamlit/secrets.toml` dan isi dengan API key Anda.

```toml
# .streamlit/secrets.toml

GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

### 4. Jalankan Aplikasi

Setelah konfigurasi selesai, jalankan perintah berikut di terminal:

```bash
streamlit run streamlit_react_tools_app.py
```

Aplikasi sekarang akan berjalan dan bisa diakses melalui browser di `http://localhost:8501`.

---

## 📁 Struktur Proyek

```
📦 career-pathfinder-ai/
├── streamlit_react_tools_app.py  # File utama aplikasi 
├── streamlit_career_pathfinder.py
├── requirements.txt           # Daftar dependensi Python
├── .streamlit/
│   └── secrets.toml           # File untuk menyimpan API Key
├── example_conversation.png
└── README.md                  
```

---

## 🔮 Rencana Pengembangan

Beberapa fitur yang dapat ditambahkan di masa depan:

* **📄 Simpan Hasil Konseling:** Menyimpan ringkasan percakapan dan roadmap sebagai file PDF.
* **📊 Visualisasi Minat:** Menampilkan visualisasi minat karier pengguna menggunakan grafik.
* **📝 AI Resume Advisor:** Fitur untuk memberikan masukan pada resume berdasarkan roadmap karier yang dihasilkan.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

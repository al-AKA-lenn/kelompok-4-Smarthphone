import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Smartphone Addiction Intelligence",
    page_icon="",
    layout="wide"
)

# --- 2. FUNGSI CAPTCHA DINAMIS ---
def generate_captcha(force=False):
    if "captcha_val" not in st.session_state or force:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 10)
        st.session_state["captcha_val"] = num1 + num2
        st.session_state["captcha_question"] = f"{num1} + {num2}"

# --- 3. FUNGSI LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # Mengacu pada file dataset yang tersedia
        df = pd.read_csv("Smartphone_Usage_And_Addiction_Analysis_7500_Rows.csv")
        return df
    except:
        return pd.DataFrame()

# --- 4. HALAMAN LOGIN ---
def login_page():
    generate_captcha()
    
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; }
        .header-container { text-align: center; margin-bottom: 30px; padding: 10px; }
        .header-title {
            font-family: 'Monospace', sans-serif;
            font-size: 36px; font-weight: bold;
            letter-spacing: 5px; color: white; margin: 0;
            text-transform: uppercase;
        }
        .header-subtitle { font-size: 16px; color: #1DB954; font-weight: bold; margin-top: 5px; }
        .narration-text {
            color: #b3b3b3; font-size: 14px; line-height: 1.6;
            max-width: 700px; margin: 20px auto; text-align: center;
        }
        .captcha-box {
            background-color: #161b22; padding: 25px; border-radius: 12px;
            text-align: center; margin: 15px 0; border: 1px solid #30363d;
        }
        .captcha-question { font-size: 32px; font-weight: bold; color: #1DB954; letter-spacing: 8px; }
        .tester-container {
            background-color: #1c2128; padding: 10px; border-radius: 8px;
            margin-bottom: 8px; border-left: 4px solid #1DB954; font-size: 13px;
        }
        .visual-narration {
            color: #b3b3b3; font-size: 13.5px; font-style: italic;
            margin-top: 10px; line-height: 1.5; padding: 15px;
            background-color: #161b22; border-radius: 8px; border-left: 3px solid #1DB954;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("###  Admin Tester")
        # Daftar akun berdasarkan data Kelompok 4
        accounts = [("admin", "12345"), ("user_01", "pass_01"), ("user_02", "pass_02"), ("user_03", "pass_03"), ("user_04", "pass_04")]
        for user, pw in accounts:
            st.markdown(f'<div class="tester-container"><b>User:</b> {user}<br><b>Pass:</b> {pw}</div>', unsafe_allow_html=True)
        st.info("Pastikan soal captcha dijawab dengan benar untuk akses sistem.")

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="header-container">
                <div class="header-title">SMARTPHONE ADDICTION</div>
                <div class="header-subtitle">Kelompok 4 • Data Visualization Dashboard</div>
                <div class="narration-text">
                    Selamat datang di sistem intelijen data kami. Dashboard ini dirancang untuk memberikan 
                    perspektif komprehensif mengenai pola adiksi smartphone pada 7500 responden. 
                    Silakan login untuk mengeksplorasi temuan data kami.
                </div>
            </div>
        """, unsafe_allow_html=True)

        u = st.text_input("Username", placeholder="Masukkan ID")
        p = st.text_input("Password", type="password", placeholder="Masukkan Pin")
        
        st.markdown(f'<div class="captcha-box"><span class="captcha-question">{st.session_state["captcha_question"]} = ?</span></div>', unsafe_allow_html=True)
        ans = st.number_input("Verifikasi: Input hasil hitungan di atas", step=1, value=0)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            if st.button(" Login Ke Dashboard", use_container_width=True, type="primary"):
                valid_accounts = dict(accounts)
                if u in valid_accounts and valid_accounts[u] == p:
                    if ans == st.session_state["captcha_val"]:
                        st.session_state["logged_in"] = True
                        st.rerun()
                    else: st.error("Jawaban Captcha tidak tepat!")
                else: st.error("Username atau Password salah!")
        with c2:
            if st.button(" Soal Baru", use_container_width=True):
                generate_captcha(force=True)
                st.rerun()

# --- 5. LOGIKA NAVIGASI ---
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# --- 6. DASHBOARD UTAMA ---
df = load_data()

if not df.empty:
    # Sidebar Kontrol Analisis
    st.sidebar.markdown("###  Kontrol Analisis")
    st.sidebar.write(f"Logged in: **Kelompok 4**")
    
    gender_options = df['gender'].unique().tolist()
    selected_gender = st.sidebar.multiselect("Filter Gender:", gender_options, default=gender_options)
    
    stress_options = df['stress_level'].unique().tolist()
    selected_stress = st.sidebar.multiselect("Filter Tingkat Stres:", stress_options, default=stress_options)
    
    age_min = int(df['age'].min())
    age_max = int(df['age'].max())
    age_range = st.sidebar.slider("Rentang Usia:", age_min, age_max, (age_min, age_max))
    
    if st.sidebar.button("Logout ", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()

    # Filter Progresif
    df_filtered = df[
        (df['gender'].isin(selected_gender)) & 
        (df['stress_level'].isin(selected_stress)) &
        (df['age'].between(age_range[0], age_range[1]))
    ]

    st.title(" Visualisasi & Analisis Naratif")
    st.markdown(f"Menampilkan hasil analisis untuk **{len(df_filtered)} responden**.")
    st.divider()

    # Visualisasi & Narasi Baris 1
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" Komposisi Gender")
        fig1, ax1 = plt.subplots()
        sns.countplot(data=df_filtered, x='gender', palette='viridis', ax=ax1)
        st.pyplot(fig1)
        st.markdown('<div class="visual-narration"><b>Narasi:</b> Grafik ini menunjukkan distribusi gender dalam sampel data. Dengan memahami komposisi ini, kita dapat menilai apakah perilaku penggunaan smartphone bersifat universal atau dipengaruhi oleh latar belakang gender.</div>', unsafe_allow_html=True)

    with col2:
        st.subheader(" Distribusi Usia")
        fig2, ax2 = plt.subplots()
        sns.histplot(df_filtered['age'], bins=15, kde=True, color='#1DB954', ax=ax2)
        st.pyplot(fig2)
        st.markdown('<div class="visual-narration"><b>Narasi:</b> Histogram usia menunjukkan kelompok umur mana yang paling dominan dalam dataset. Puncak grafik menandakan generasi yang paling aktif menggunakan teknologi smartphone saat ini.</div>', unsafe_allow_html=True)

    st.divider()
    
    # Visualisasi & Narasi Baris 2
    col3, col4 = st.columns(2)
    with col3:
        st.subheader(" Stres vs Status Adiksi")
        fig3, ax3 = plt.subplots()
        sns.countplot(data=df_filtered, x='stress_level', hue='addicted_label', palette='coolwarm', ax=ax3)
        st.pyplot(fig3)
        st.markdown('<div class="visual-narration"><b>Narasi:</b> Korelasi antara kesehatan mental dan adiksi terlihat di sini. Tingkat stres yang lebih tinggi seringkali berkaitan dengan kecenderungan individu untuk mencari pelarian melalui layar smartphone secara berlebihan.</div>', unsafe_allow_html=True)

    with col4:
        st.subheader(" Analisis Durasi Layar")
        fig4, ax4 = plt.subplots()
        sns.boxplot(data=df_filtered, x='addicted_label', y='daily_screen_time_hours', palette='magma', ax=ax4)
        st.pyplot(fig4)
        st.markdown('<div class="visual-narration"><b>Narasi:</b> Melalui boxplot, kita dapat melihat sebaran jam penggunaan harian. Perbedaan mencolok antara median durasi layar kelompok "Addicted" dan "Non-Addicted" menjadi bukti nyata adanya pola penggunaan yang tidak sehat.</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- 7. DATA MENTAH (RAW DATA) ---
    st.subheader(" Eksplorasi Data Lanjutan")
    with st.expander(" Klik untuk Melihat Data Mentah (Raw Data)"):
        st.write("Tabel di bawah ini menampilkan 50 baris pertama dari data yang telah difilter:")
        st.dataframe(df_filtered.head(50), use_container_width=True)
        st.info(f"Rata-rata penggunaan layar dari filter saat ini: {df_filtered['daily_screen_time_hours'].mean():.2f} jam/hari.")

else:
    st.error("Gagal memuat dataset. Pastikan file 'Smartphone_Usage_And_Addiction_Analysis_7500_Rows.csv' tersedia di direktori proyek.")

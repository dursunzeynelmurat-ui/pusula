import streamlit as st
import google.generativeai as genai
import time
import datetime

# --- SAYFA AYARLARI ---
# Yan paneli gizle ve sayfayı ortala
st.set_page_config(
    page_title="Pusula AI - Sanal Psikolog",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CSS TASARIM (Pusula Renkleri ve Animasyonlar) ---
st.markdown("""
<style>
    /* Genel Arkaplan */
    .stApp { background-color: #F5F5F0; }
    
    /* Başlıklar */
    h1, h2, h3 { color: #2C3E50 !important; font-family: 'Helvetica', sans-serif; font-weight: 300; }
    
    /* Chat Balonları */
    .stChatMessage { background-color: white; border-radius: 15px; padding: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    
    /* Nefes Animasyonu */
    @keyframes breath {
        0% { transform: scale(1); opacity: 0.8; }
        40% { transform: scale(1.8); opacity: 1; }
        60% { transform: scale(1.8); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    .breathing-circle {
        width: 150px; height: 150px; background-color: #8DA399; border-radius: 50%;
        margin: 50px auto; animation: breath 12s infinite ease-in-out;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 16px; box-shadow: 0 0 20px rgba(141, 163, 153, 0.4);
    }
    
    /* Panik Butonu */
    .big-button > button {
        width: 100%; height: 70px; background-color: #E07A5F; color: white;
        font-size: 20px; border-radius: 15px; border: none;
    }
</style>
""", unsafe_allow_html=True) 

# --- SESSION STATE (Hafıza) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'messages' not in st.session_state:
    # AI'a kim olduğunu öğretiyoruz (Sistem Mesajı)
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Sen 'Pusula' adında sanal bir psikolojik destek asistanısın. 
            Görevin: Kullanıcıyı Bilişsel Davranışçı Terapi (BDT) teknikleriyle dinlemek, sakinleştirmek ve farkındalık kazandırmak.
            Kurallar:
            1. Asla tıbbi teşhis koyma.
            2. Çok uzun cevaplar verme, sohbet havasında kal.
            3. Tonun sakin, şefkatli, yargısız ve "sen" diliyle olsun.
            4. Eğer kullanıcı intihar veya kendine zarar vermekten bahsederse, nazikçe profesyonel yardım alması gerektiğini söyle (Örn: 'Bu duygularla yalnız değilsin, lütfen hemen bir uzmandan destek al.') ve sohbeti orada yönlendir.
            5. Kullanıcıya sorular sorarak onu kendi çözümlerini bulmaya yönelt."""
        }
    ]
if 'worries' not in st.session_state:
    st.session_state.worries = []
if 'model' not in st.session_state:
    st.session_state.model = None

# --- YARDIMCI FONKSİYONLAR ---
def go_home(): st.session_state.page = 'home'
def go_panic(): st.session_state.page = 'panic'
def go_chat(): st.session_state.page = 'chat'
def go_worry(): st.session_state.page = 'worry'

# --- API KEY KONTROLÜ VE GEMINI BAĞLANTISI (Güvenli Blok) ---
if st.session_state.model is None:
    if "api_keys" in st.secrets and "gemini" in st.secrets["api_keys"]:
        gemini_api_key = st.secrets["api_keys"]["gemini"]
        
        try:
            genai.configure(api_key=gemini_api_key)
            st.session_state.model = genai.GenerativeModel('gemini-pro') 
            
        except Exception as e:
            # Hata oluşursa, model None kalır ve hata mesajı ekrana basılır
            st.error(f"API BAĞLANTI HATASI (Geliştirici Notu): {e}") 
    
# ==========================================
# SAYFA 1: ANA EKRAN
# ==========================================
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align: center;'>Pusula AI 🧭</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Yapay Zeka Destekli İçsel Yolculuk</p>", unsafe_allow_html=True)
    st.write("---")
    
    # API Bağlantı Durumu Kontrolü
    if st.session_state.model is None:
        st.error("Uygulama sahibi: Gemini AI bağlantısı kurulamadı. Lütfen secrets.toml dosyanızı kontrol edin.")
    else:
        st.success("Sistem hazır. Rehberle konuşmaya başlayabilirsin. ✅")

    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button("MERKEZE DÖN (PANİK)"):
            go_panic()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("Kalp atışın hızlandıysa veya bunalmış hissediyorsan tıkla.")
        
        st.write("") # Boşluk
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💬 AI Rehberle Konuş", use_container_width=True):
                if st.session_state.model is None:
                    st.error("Bağlantı sorunu nedeniyle sohbet başlatılamıyor.")
                else:
                    go_chat()
                    st.rerun()
        with c2:
            if st.button("📦 Endişe Kutusu", use_container_width=True):
                go_worry()
                st.rerun()

# ==========================================
# SAYFA 2: GEMINI SOHBET (AI REHBER)
# ==========================================
elif st.session_state.page == 'chat':
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("⬅️"): go_home(); st.rerun()
    with c2:
        st.markdown("### Rehber (AI)")

    # Model kontrolü
    if st.session_state.model is None:
        st.error("Uygulama sunucusu API anahtarını yükleyemedi. Lütfen Ana Ekrana dönün.")
        st.stop()

    # Sohbet Geçmişini Ekrana Bas (Sistem mesajı hariç)
    for message in st.session_state.messages:
        if message["role"] != "system": 
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Kullanıcıdan Girdi Al
    if prompt := st.chat_input("Neler hissediyorsun

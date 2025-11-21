import streamlit as st
import google.generativeai as genai
import time
import datetime

# --- SAYFA AYARLARI ---
# Yan paneli gizle ve sayfayı ortala
st.set_page_config(
    page_title="Pusula - İçindeki Yön",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CSS TASARIM (Butonlar Kırmızı ve Büyük) ---
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
    
    /* ODAKLAN Butonu (Kırmızı, Büyük ve Merkezde) */
    .big-button > button {
        width: 100%; 
        height: 100px; /* Butonu uzun yaptık */
        background-color: #C0392B; /* Canlı Kırmızı */
        color: white;
        font-size: 24px; /* Yazıyı büyüttük */
        border-radius: 15px; 
        border: none;
        transition: background-color 0.3s;
    }
    .big-button > button:hover {
        background-color: #E74C3C; /* Mouse üzerine gelince rengi açılır */
    }
</style>
""", unsafe_allow_html=True) 

# --- SESSION STATE (Hafıza) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'messages' not in st.session_state:
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
            # 💡 Hata düzeltmesi: Model adı 'gemini-2.5-flash' olarak güncellendi.
            st.session_state.model = genai.GenerativeModel('gemini-2.5-flash') 
            
        except Exception as e:
            st.error(f"API BAĞLANTI HATASI (Geliştirici Notu): {e}") 
    
# ==========================================
# SAYFA 1: ANA EKRAN
# ==========================================
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align: center;'>Pusula 🧭</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Yapay Zeka Destekli İçsel Yolculuk</p>", unsafe_allow_html=True)
    st.write("---")
    
    # API Bağlantı Durumu Kontrolü
    if st.session_state.model is None:
        st.error("Uygulama sahibi: Gemini AI bağlantısı kurulamadı. Lütfen secrets.toml dosyanızı kontrol edin.")
    else:
        st.success("Sistem hazır. Rehberle konuşmaya başlayabilirsin. ✅")

    # --- ODAKLAN BUTONU (Sayfanın Ortası) ---
    st.write("") 
    col_center1, col_center2, col_center3 = st.columns([1, 4, 1]) 
    
    with col_center2: 
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button("ŞİMDİ ODAKLAN", key="panic_button"):
            go_panic()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("Kalp atışın hızlandıysa veya bunalmış hissediyorsan hemen tıkla.")
    
    st.write("---")
    
    # --- ALT MENÜ BUTONLARI ---
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 Rehberle Konuş", use_container_width=True): 
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
# SAYFA 2: GEMINI SOHBET (REHBER)
# ==========================================
elif st.session_state.page == 'chat':
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("⬅️"): go_home(); st.rerun()
    with c2:
        st.markdown("### Rehber")

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
    if prompt := st.chat_input("Neler hissediyorsun?"):
        # 1. Kullanıcı mesajını göster ve kaydet
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2. Sohbet Geçmişini Hazırla
        contents = []
        for msg in st.session_state.messages:
            role = 'user' if msg['role'] in ['user', 'system'] else 'model'
            contents.append({'role': role, 'parts': [{'text': msg['content']}]})
        
        try:
            response = st.session_state.model.generate_content(contents)
            ai_reply = response.text

            # 3. AI Cevabını göster ve kaydet
            with st.chat_message("assistant"):
                st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        except Exception as e:
            st.error("Bağlantı hatası veya token limiti aşıldı.")
            st.error(f"Detay: {e}")


# ==========================================
# SAYFA 3: NEFES (PANİK)
# ==========================================
elif st.session_state.page == 'panic':
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("⬅️"): go_home(); st.rerun()
    
    st.markdown("<h2 style='text-align: center;'>Sadece Daireye Bak</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="breathing-circle">
            Nefes Al...
        </div>
        <p style='text-align: center; margin-top: 20px; color: #555;'>
        4 saniye al • 4 saniye tut • 4 saniye ver
        </p>
    """, unsafe_allow_html=True)
    
    # 5-4-3-2-1 Tekniği
    with st.expander("Hala sakinleşemedin mi? Topraklanma Tekniğini dene 👇"):
        st.write("👀 **5** tane gördüğün şey")
        st.write("🖐️ **4** tane dokunduğun şey")
        st.write("👂 **3** tane duyduğun ses")
        st.write("👃 **2** tane kokladığın şey")
        st.write("👅 **1** tane tattığın şey")


# ==========================================
# SAYFA 4: ENDİŞE KUTUSU
# ==========================================
elif st.session_state.page == 'worry':
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("⬅️"): go_home(); st.rerun()
    with c2:
        st.markdown("### Endişe Kutusu 📦")

    st.info("Zihninden atamadığın düşünceleri buraya yaz ve 'Kutuya At' de. Artık onları taşımak zorunda değilsin.")

    with st.form("worry_form", clear_on_submit=True):
        text = st.text_area("Seni rahatsız eden düşünceyi buraya bırak:", height=100)
        submitted = st.form_submit_button("Kutuya At ve Kilitle")
        if submitted and text:
            now = datetime.datetime.now().strftime("%d/%m %H:%M")
            st.session_state.worries.insert(0, {"text": text, "date": now})
            st.success("Düşünce kutuya atıldı. Şimdi rahatlayabilirsin.")

    st.write("---")
    if st.session_state.worries:
        st.caption("Kutudakiler:")
        for w in st.session_state.worries:
            st.info(f"📅 {w['date']}\n\n{w['text']}")
    else:
        st.caption("Kutu boş. Zihnin sakin görünüyor.")

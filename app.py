import streamlit as st
import google.generativeai as genai
# ... (Diğer importlar) ...

# --- API KEY KONTROLÜ VE GEMINI BAĞLANTISI (Sadece Secrets Kullanarak) ---

# Model bağlantı durumunu tutmak için session state kullanıyoruz
if 'model' not in st.session_state:
    st.session_state.model = None
    
if "api_keys" in st.secrets and "gemini" in st.secrets["api_keys"]:
    gemini_api_key = st.secrets["api_keys"]["gemini"]
    
    try:
        genai.configure(api_key=gemini_api_key)
        st.session_state.model = genai.GenerativeModel('gemini-pro')
        
        # Bu mesajı sadece uygulama sahibi görsün diye sidebar'a koyuyoruz
        st.sidebar.success("Gemini bağlantısı başarıyla kuruldu.", icon="✅")
    
    except Exception:
        st.sidebar.error("API Anahtarı geçersiz. Lütfen secrets dosyasını kontrol edin.")
        st.session_state.model = None
else:
    st.sidebar.warning("Uygulama Sahibi: API anahtarı secrets dosyasında bulunamadı. Uygulama çalışmayabilir.")
    st.session_state.model = None

# ... (Kodun devamı) ...

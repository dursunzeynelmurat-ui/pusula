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
# Üçlü tırnak işaretleri doğru kapatıldı.
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
""", unsafe_allow_html=True) # <-- Hatanın çözüldüğü yer burasıdır.

# ---

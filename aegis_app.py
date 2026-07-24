# aegis_app.py
import streamlit as st
import numpy as np
import pandas as pd
from modules.crypto_shield import CryptoShield
import database as db  # <-- Importa seu banco de dados

st.set_page_config(page_title="AEGIS Sentinel", layout="wide")

# Inicializa banco
db.init_db()
if not db.carregar_dispositivos():
    db.salvar_dispositivo("TOK-CAM-001", "BodyCam Turno A", "BodyCam / Arquivo Gravado", "WIN_2024.mp4")

if "crypto" not in st.session_state:
    st.session_state.crypto = CryptoShield()

dispositivos_db = db.carregar_dispositivos()

# Menu e Interface do Streamlit
st.sidebar.title("🛡️ AEGIS Sentinel")
token_ativo = st.sidebar.selectbox("Câmeras:", options=list(dispositivos_db.keys()))
dev_info = dispositivos_db[token_ativo]

st.title("📹 Painel de Monitoramento")
tab_analise, tab_banco = st.tabs(["🎥 Análise", "🗄️ Banco de Dados"])

with tab_analise:
    if st.button("Executar Análise", type="primary"):
        matrix = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        ai_res = {"status": "Inconsistência Detectada", "camera": dev_info['nome']}
        proof = st.session_state.crypto.generate_proof(dev_info, ai_res, matrix)
        st.success("Análise executada com sucesso!")
        st.code(proof[:100], language="text")

with tab_banco:
    st.subheader("Dispositivos no SQLite")
    df = pd.DataFrame.from_dict(dispositivos_db, orient="index")
    st.dataframe(df, use_container_width=True)

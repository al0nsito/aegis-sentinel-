import streamlit as st
import numpy as np
from modules.crypto_shield import CryptoShield

st.set_page_config(page_title="AEGIS Sentinel Server Interface", layout="wide")

# Instancia o módulo criptográfico no session_state
if "crypto" not in st.session_state:
    st.session_state.crypto = CryptoShield()

# Dicionário de Câmeras e Hardwares por Token
if "camera_tokens" not in st.session_state:
    st.session_state.camera_tokens = {
        "TOK-CAM-CORP-001": {
            "nome": "BodyCam Turno A [CAM-CORP-001]",
            "tipo": "BodyCam / Arquivo Gravado",
            "origem": "WIN_2024_Pro.mp4",
            "status": "Ativo"
        },
        "TOK-RTSP-GATE-02": {
            "nome": "Câmera IP - Portaria Principal",
            "tipo": "Stream RTSP / IP",
            "origem": "rtsp://192.168.1.100:554/live",
            "status": "Ativo"
        }
    }

# ==============================================================================
# BARRA LATERAL (GESTAO DE HARDAWARE E TOKENS)
# ==============================================================================
st.sidebar.title("🛡️ AEGIS Sentinel")
st.sidebar.subheader("📡 Central de Câmeras & Hardware")

token_ativo = st.sidebar.selectbox(
    "Dispositivo Autorizado / Token:",
    options=list(st.session_state.camera_tokens.keys())
)

dev_info = st.session_state.camera_tokens[token_ativo]

st.sidebar.success(
    f"**Dispositivo:** {dev_info['nome']}\n\n"
    f"**Tipo:** {dev_info['tipo']}"
)

# Painel No-Code para Adicionar Novas Câmeras via Token
with st.sidebar.expander("➕ Cadastrar Nova Câmera / Hardware"):
    novo_token_id = st.text_input("ID do Token:", value="TOK-CAM-003")
    nome_dev = st.text_input("Nome da Câmera:", value="Câmera Galpão Leste")
    tipo_dev = st.selectbox("Tipo de Conexão:", ["Stream RTSP / IP", "BodyCam / Arquivo Gravado", "Webcam USB"])
    origem_dev = st.text_input("URI / IP / Arquivo:", value="rtsp://192.168.1.150:554/live")

    if st.button("Salvar e Ativar Câmera"):
        st.session_state.camera_tokens[novo_token_id] = {
            "nome": nome_dev, "tipo": tipo_dev, "origem": origem_dev, "status": "Ativo"
        }
        st.sidebar.success(f"Câmera '{nome_dev}' cadastrada com sucesso!")
        st.rerun()

# ==============================================================================
# PAINEL PRINCIPAL DE PROCESSAMENTO
# ==============================================================================
st.title("📹 Monitoramento & Fiscalização em Tempo Real")

st.markdown("---")

st.subheader("2. Entrada de Mídia Universal")
uploaded_file = st.file_uploader("Envie o arquivo de mídia:", type=["mp4", "avi", "mov"])

simular_epi = st.checkbox("Simular Desvio de Segurança (EPI)", value=True)
iniciar_analise = st.button("Iniciar Análise de Vídeo", type="primary")

if iniciar_analise:
    if uploaded_file is not None or dev_info["tipo"] == "Stream RTSP / IP":
        # Simulação de captura de frame (matriz OpenCV 640x480)
        matrix = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        ai_res = {
            "status": "Inconsistência Detectada" if simular_epi else "Normal",
            "infracao": "EPI Ausente (Capacete de Segurança)" if simular_epi else "Nenhuma",
            "dispositivo": dev_info['nome'],
            "token": token_ativo
        }

        try:
            # Chamada da função que anteriormente falhava por causa do ndarray
            proof = st.session_state.crypto.generate_proof(dev_info, ai_res, matrix)
            
            st.success("✅ Análise concluída e prova criptográfica gerada com sucesso!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Resultado da Fiscalização")
                st.json(ai_res)
            with col2:
                st.subheader("Prova de Integridade (Crypto Shield)")
                st.info(f"Tamanho do Payload Gerado: {len(proof)} bytes")
                st.code(f"Hash/Bytes: {proof[:120]}...", language="text")

        except Exception as e:
            st.error(f"Erro no processamento: {e}")
    else:
        st.warning("Por favor, selecione um arquivo de vídeo para realizar a análise.")

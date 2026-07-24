import streamlit as st
import time
import json
import numpy as np

from modules.device_auth import DeviceAuthenticator
from modules.universal_decoder import UniversalDecoder
from modules.matrix_adapter import DynamicMatrixAdapter
from modules.ai_engine import AdaptiveAIEngine
from modules.crypto_shield import LegalCryptoShield
from modules.ram_vault import RAMVault

# Configuração da Interface
st.set_page_config(page_title="AEGIS Sentinel — Autenticação & Matrizes Dinâmicas", layout="wide")

# Carregar Configuração
with open("aegis_config.json") as f:
    config = json.load(f)

# Inicializar Estado
if "vault" not in st.session_state:
    st.session_state.vault = RAMVault()
if "crypto" not in st.session_state:
    st.session_state.crypto = LegalCryptoShield()
if "authenticator" not in st.session_state:
    st.session_state.authenticator = DeviceAuthenticator(config["authorized_devices"])
if "decoder" not in st.session_state:
    st.session_state.decoder = UniversalDecoder()
if "infraction_start_time" not in st.session_state:
    st.session_state.infraction_start_time = None

adapter = DynamicMatrixAdapter(max_side_px=config["system"]["max_matrix_side_px"])
ai_engine = AdaptiveAIEngine()

st.title("🛡️ AEGIS Sentinel — Sistema de Governança Ocupacional")
st.caption("Validação de Dispositivos | Processamento com Matriz Dinâmica | 0% Uso de Disco")

# 1. PAINEL LATERAL: AUTENTICAÇÃO DO DISPOSITIVO
st.sidebar.header("🔑 1. Autenticação do Dispositivo")
device_token = st.sidebar.text_input("Insira o Token do Dispositivo/Aparelho:", value="TOK-883921-A")

is_auth, auth_msg, dev_info = st.session_state.authenticator.validate_device(device_token)

if is_auth:
    st.sidebar.success(auth_msg)
else:
    st.sidebar.error(auth_msg)
    st.error("⛔ ACESSO BLOQUEADO: Conecte ou autentique um dispositivo válido na barra lateral para liberar a análise.")
    st.stop()

st.sidebar.markdown("---")

# 2. PAINEL LATERAL: FONTE DE MÍDIA
st.sidebar.header("📹 2. Entrada de Mídia Universal")
input_type = st.sidebar.selectbox("Tipo de Sinal/Mídia:", ["Arquivo Gravado (Qualquer Extensão)", "Stream de Câmera (USB / IP)"])

media_ready = False

if input_type == "Arquivo Gravado (Qualquer Extensão)":
    uploaded_file = st.sidebar.file_uploader(
        "Envie o arquivo de mídia:", 
        type=["mp4", "mkv", "avi", "mov", "webm", "flv", "m4v", "3gp"]
    )
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1]
        media_ready = st.session_state.decoder.load_file_from_bytes(uploaded_file.read(), file_ext)

else:
    stream_url = st.sidebar.text_input("Endereço USB (/dev/video0 ou 0) ou URL Stream IP:", value="0")
    if st.sidebar.button("Conectar ao Dispositivo"):
        media_ready = st.session_state.decoder.load_stream_or_device(stream_url)

st.sidebar.markdown("---")
sim_infraction = st.sidebar.checkbox("Simular Desvio de Segurança (EPI)", value=False)
run_pipeline = st.sidebar.toggle("Iniciar Análise de Vídeo", value=True)

# LAYOUT PRINCIPAL
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.subheader("📺 Processamento de Matriz Adaptativa em RAM")
    frame_placeholder = st.empty()
    metrics_container = st.empty()

with col_right:
    st.subheader("⚖️ Decisão de Bifurcação & Audit Log")
    status_placeholder = st.empty()
    table_placeholder = st.empty()

# PIPELINE DE EXECUÇÃO
if run_pipeline and media_ready:
    ret, raw_frame = st.session_state.decoder.get_next_frame()

    if ret and raw_frame is not None:
        loop_start = time.time()

        # A. Adaptação Dinâmica de Matriz
        matrix, matrix_meta = adapter.process(raw_frame)

        # B. Inferência de IA
        ai_res = ai_engine.run_inference(matrix, force_infraction_simulation=sim_infraction)

        # Renderização do Frame na Tela
        frame_placeholder.image(matrix, channels="RGB", use_container_width=True)

        # Exibição de Métricas
        with metrics_container.container():
            m1, m2, m3 = st.columns(3)
            m1.metric("Resolução Original", matrix_meta["original_resolution"])
            m2.metric("Matriz Adaptada (RAM)", matrix_meta["processed_resolution"])
            m3.metric("Latência do Frame", f"{ai_res['latency_ms']:.2f} ms")

        # C. Lógica de Bifurcação e Histerese
        if ai_res["infraction"]:
            if st.session_state.infraction_start_time is None:
                st.session_state.infraction_start_time = time.time()

            elapsed_infraction = time.time() - st.session_state.infraction_start_time

            if elapsed_infraction >= config["system"]["hysteresis_threshold_sec"]:
                # BIFURCAÇÃO B: INFRAÇÃO CONFIRMADA (>3s)
                proof = st.session_state.crypto.generate_proof(dev_info, ai_res, matrix)
                
                st.session_state.vault.log_event(
                    dev_info["device_name"],
                    "INFRAÇÃO CONFIRMADA",
                    proof["hash_sha256"],
                    f"Ausência de: {', '.join(ai_res['missing_epi'])}"
                )
                status_placeholder.error(f"🚨 INFRAÇÃO REGISTRADA! Hash: {proof['hash_sha256'][:16]}...")
            else:
                status_placeholder.warning(f"⚠️ Análise de Histerese: {elapsed_infraction:.1f}s / {config['system']['hysteresis_threshold_sec']}s")
        else:
            # BIFURCAÇÃO A: COMPLIANCE
            st.session_state.infraction_start_time = None
            status_placeholder.success(f"✅ OPERADOR PROTEGIDO — Dispositivo: {dev_info['device_name']}")

        # Atualização da Tabela de Logs na RAM
        table_placeholder.dataframe(st.session_state.vault.get_dataframe(), use_container_width=True)

        # Manutenção de 1 FPS
        processing_time = time.time() - loop_start
        sleep_time = max(0.0, (1.0 / config["system"]["fps_target"]) - processing_time)
        time.sleep(sleep_time)
        st.rerun()
    else:
        frame_placeholder.info("Aguardando quadros do arquivo ou stream selecionado...")
elif not media_ready:
    st.info("Aguardando carregamento de mídia do dispositivo autenticado...")

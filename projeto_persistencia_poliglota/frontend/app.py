
import streamlit as st
import requests
import pandas as pd

# URL da API (ajuste se necessário)
API_URL = "http://localhost:8000"

# ------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------
st.set_page_config(
    page_title="Persistência Poliglota",
    page_icon="🌍",
    layout="wide"
)

# CSS customizado
st.markdown("""
    <style>
    .stButton button {
        background-color: #2E86C1;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
    }
    .stButton button:hover {
        background-color: #1B4F72;
        color: white;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🌍 Projeto de Persistência Poliglota</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>SQLite + MongoDB + GeoProcessamento</p>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------------
# MENU LATERAL
# ------------------------------
menu = st.sidebar.radio("📌 Navegar", [
    "🏛 Inserir Estado/Cidade",
    "📌 Inserir Local",
    "🗺 Ver Locais por Cidade",
    "📍 Busca por Proximidade"
])

# ------------------------------
# INSERIR ESTADO / CIDADE
# ------------------------------
if menu == "🏛 Inserir Estado/Cidade":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cadastrar Estado")
        nome_estado = st.text_input("Nome do Estado")
        if st.button("Salvar Estado", use_container_width=True):
            if not nome_estado.strip():
                st.warning("Preencha o nome do estado.")
            else:
                r = requests.post(f"{API_URL}/estado", json={"nome": nome_estado.strip()})
                if r.ok:
                    st.success(f"Estado salvo: {r.json()}")
                else:
                    st.error(f"Erro: {r.text}")

    with col2:
        st.subheader("Cadastrar Cidade")
        nome_cidade = st.text_input("Nome da Cidade", key="cidade_input")
        estado_id = st.number_input("ID do Estado (ver em /cidades)", min_value=0, step=1)
        if st.button("Salvar Cidade", use_container_width=True):
            if not nome_cidade.strip() or estado_id <= 0:
                st.warning("Forneça nome da cidade e um estado_id válido (>0).")
            else:
                payload = {"nome": nome_cidade.strip(), "estado_id": int(estado_id)}
                r = requests.post(f"{API_URL}/cidade", json=payload)
                if r.ok:
                    st.success(f"Cidade salva: {r.json()}")
                else:
                    st.error(f"Erro: {r.text}")

# ------------------------------
# INSERIR LOCAL (MONGO)
# ------------------------------
elif menu == "📌 Inserir Local":
    st.subheader("Cadastrar Local (MongoDB)")

    # pegar lista de cidades para o selectbox
    r = requests.get(f"{API_URL}/cidades")
    cidades = r.json() if r.ok else []
    if not cidades:
        st.warning("Cadastre pelo menos uma cidade primeiro.")
    else:
        opcoes = {f'{c["cidade"]} ({c["estado"]})': c["cidade"] for c in cidades}
        escolha = st.selectbox("Selecione a Cidade", list(opcoes.keys()))

        nome = st.text_input("Nome do Local", key="local_nome")
        lat = st.number_input("Latitude", format="%.6f", key="local_lat")
        lon = st.number_input("Longitude", format="%.6f", key="local_lon")
        descricao = st.text_area("Descrição (opcional)", key="local_desc")

        if st.button("Salvar Local", use_container_width=True):
            if not nome:
                st.warning("Preencha o nome do local.")
            else:
                payload = {
                    "nome_local": nome,
                    "cidade": opcoes[escolha],
                    "coordenadas": {"latitude": float(lat), "longitude": float(lon)},
                    "descricao": descricao
                }
                r = requests.post(f"{API_URL}/local", json=payload)
                if r.ok:
                    st.success(f"Local salvo: {r.json()}")
                else:
                    st.error(f"Erro: {r.text}")

# ------------------------------
# VER LOCAIS POR CIDADE
# ------------------------------
elif menu == "🗺 Ver Locais por Cidade":
    st.subheader("Locais por Cidade")

    # pegar lista de cidades do backend
    r = requests.get(f"{API_URL}/cidades")
    cidades = r.json() if r.ok else []
    if not cidades:
        st.warning("Nenhuma cidade cadastrada ainda.")
    else:
        opcoes = {f'{c["cidade"]} ({c["estado"]})': c["id"] for c in cidades}
        escolha = st.selectbox("Selecione uma cidade", list(opcoes.keys()))

        if st.button("Buscar", use_container_width=True):
            cidade_id = opcoes[escolha]
            r2 = requests.get(f"{API_URL}/cidades/{cidade_id}/locais")
            if r2.ok:
                dados = r2.json()
                locais = dados["locais"]
                if not locais:
                    st.info("Nenhum local encontrado para esta cidade.")
                else:
                    df = pd.DataFrame([{
                        "nome_local": d.get("nome_local"),
                        "cidade": d.get("cidade"),
                        "latitude": d.get("coordenadas", {}).get("latitude"),
                        "longitude": d.get("coordenadas", {}).get("longitude"),
                        "descricao": d.get("descricao")
                    } for d in locais])
                    with st.expander("📍 Resultados da Busca"):
                        st.dataframe(df, use_container_width=True)
                        mapa = df.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]].dropna()
                        if not mapa.empty:
                            st.map(mapa)
            else:
                st.error("Erro ao buscar locais.")

# ------------------------------
# BUSCA POR PROXIMIDADE
# ------------------------------
elif menu == "📍 Busca por Proximidade":
    st.subheader("Buscar locais próximos")
    lat = st.number_input("Latitude", format="%.6f", key="p_lat")
    lon = st.number_input("Longitude", format="%.6f", key="p_lon")
    raio = st.number_input("Raio (km)", min_value=0.1, value=10.0, step=0.1, key="p_raio")

    if st.button("Pesquisar", use_container_width=True):
        r = requests.get(f"{API_URL}/locais/proximos", params={"lat": lat, "lon": lon, "raio_km": raio})
        if r.ok:
            docs = r.json()
            if not docs:
                st.info("Nenhum local encontrado no raio informado.")
            else:
                df = pd.DataFrame([{
                    "nome_local": d.get("nome_local"),
                    "cidade": d.get("cidade"),
                    "latitude": d.get("coordenadas", {}).get("latitude"),
                    "longitude": d.get("coordenadas", {}).get("longitude"),
                    "distancia_km": d.get("distancia_km"),
                    "descricao": d.get("descricao")
                } for d in docs])
                with st.expander("📍 Resultados da Busca"):
                    st.dataframe(df, use_container_width=True)
                    mapa = df.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]].dropna()
                    if not mapa.empty:
                        st.map(mapa)
        else:
            st.error("Erro na requisição.")

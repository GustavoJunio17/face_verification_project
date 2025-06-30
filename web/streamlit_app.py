import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("Sistema de Cadastro e Login Facial")
menu = st.sidebar.selectbox("Menu", ["Cadastro", "Login"])

def enviar_cadastro(nome, email, senha, imagem):
    files = {"imagem": ("foto.jpg", imagem, "image/jpeg")}
    data = {"nome": nome, "email": email, "senha": senha}
    return requests.post(f"{API_BASE}/cadastrar", data=data, files=files)

def enviar_login(email, senha, imagem):
    files = {"imagem": ("foto.jpg", imagem, "image/jpeg")}
    data = {"email": email, "senha": senha}
    return requests.post(f"{API_BASE}/verificar", data=data, files=files)

if menu == "Cadastro":
    st.header("Cadastro")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    foto = st.camera_input("Tire uma foto")

    if st.button("Cadastrar"):
        if not nome or not email or not senha or foto is None:
            st.error("Preencha todos os campos e tire a foto.")
        else:
            img_bytes = foto.getvalue()
            res = enviar_cadastro(nome, email, senha, img_bytes)
            if res.status_code == 200:
                st.success("Cadastro realizado com sucesso!")
            else:
                st.error(f"Erro: {res.json().get('detail')}")

elif menu == "Login":
    st.header("Login Facial")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    foto = st.camera_input("Tire uma foto para login")

    if st.button("Entrar"):
        if not email or not senha or foto is None:
            st.error("Preencha email, senha e tire a foto.")
        else:
            img_bytes = foto.getvalue()
            res = enviar_login(email, senha, img_bytes)
            res_json = res.json()
            if res.status_code == 200 and res_json.get("match"):
                st.success(res_json["mensagem"])
            else:
                st.warning(res_json.get("mensagem", "Login falhou."))
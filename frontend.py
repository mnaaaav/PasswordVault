import streamlit as st
import requests

st.title("🔐 Secure Password Vault")

menu = ["Store Password", "Retrieve Password"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Store Password":
    st.subheader("Store a New Password")
    website = st.text_input("Website")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Store"):
        response = requests.post("http://127.0.0.1:8000/store/", json={
            "website": website,
            "username": username,
            "password": password
        })
        st.success(response.json()["message"])

elif choice == "Retrieve Password":
    st.subheader("Retrieve Stored Password")
    website = st.text_input("Enter Website Name")
    
    if st.button("Retrieve"):
        response = requests.get(f"http://127.0.0.1:8000/retrieve/{website}")
        if response.status_code == 200:
            data = response.json()
            st.write(f"**Website:** {data['website']}")
            st.write(f"**Username:** {data['username']}")
            st.write(f"**Password:** {data['password']}")
        else:
            st.error("No password found for this website.")

import streamlit as st
import requests

st.title("Password Vault")

# User authentication
username = st.text_input("Enter Username", key="username_input")
password = st.text_input("Enter Password", type="password", key="password_input")

# Login/Register buttons
if st.button("Register"):
    response = requests.post("http://127.0.0.1:8000/register", json={"username": username, "password": password})
    st.success(response.json().get("message", "Error"))

if st.button("Login"):
    response = requests.post("http://127.0.0.1:8000/login", json={"username": username, "password": password})
    if response.status_code == 200:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success(response.json().get("message", "Login successful"))
    else:
        st.error(response.json().get("detail", "Login failed"))

# If logged in, show options to store/retrieve passwords
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.subheader("Store a New Password")
    website = st.text_input("Enter Website", key="website_input")
    account_username = st.text_input("Enter Account Username", key="account_username_input")
    account_password = st.text_input("Enter Password", type="password", key="account_password_input")

    if st.button("Store Password"):
        response = requests.post("http://127.0.0.1:8000/store", 
                                 json={"website": website, "username": account_username, "password": account_password})
        st.success(response.json()["message"])

    st.subheader("Retrieve Stored Passwords")
    if st.button("Show Stored Passwords"):
        response = requests.get("http://127.0.0.1:8000/retrieve")
        if response.status_code == 200:
            passwords = response.json()["passwords"]
            for entry in passwords:
                st.write(f"Website: {entry['website']} | Username: {entry['username']} | Password: {entry['password']}")

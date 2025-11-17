import streamlit as st
import requests

FIREBASE_API_KEY = st.secrets.get("firebase_api_key")
FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

# -------------------------------
# Authenticate User 
# signUp or signInWithPassword
# -------------------------------
def authenticate(email: str, password: str, method: str):
    url = f"{FIREBASE_AUTH_URL}:{method}?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    data = response.json()

    # Auth was unsuccessful
    if "error" in data:
        message = data["error"]["message"]
        if ("EMAIL_EXISTS" in message):
            message = "Email already exists, please login instead."
        elif ("INVALID_EMAIL" in message):
            message = "Email is invalid."
        elif ("WEAK_PASSWORD" in message):
            message = "Password should be at least 6 characters"
        elif ("INVALID_LOGIN_CREDENTIALS" in message):
            message = "Either email or password is incorrect."
        st.session_state.toast = {
            "message": f"Failed to authenticate user {email}. {message}",
            "icon": ":material/error:"
        }

    # Auth was successful
    else:
        st.session_state.user = data["email"]
        st.session_state.id_token = data["idToken"]
        st.session_state.refresh_token = data["refreshToken"]
        st.session_state.local_id = data["localId"]
        st.session_state.toast = {
            "message": f"Successfully logged in as user {email}",
            "icon": ":material/check:"
        }
        st.session_state.load_chats = True

# -------------------------------
# Refresh the Firebase ID token
# -------------------------------
def refresh_id_token():
    url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": st.session_state.refresh_token
    }

    resp = requests.post(url, data=data).json()

    st.session_state.id_token = resp["id_token"]
    st.session_state.refresh_token = resp["refresh_token"]
    st.session_state.local_id = resp["user_id"]

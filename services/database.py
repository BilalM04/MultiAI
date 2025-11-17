import streamlit as st
import json
import time
import requests
from services.authentication import authenticate, refresh_id_token

PROJECT_ID = st.secrets["firebase_project_id"]

# ---------------------------------------
# Save chat to DB for current user
# ---------------------------------------
def save_chat(chat_name: str, chat_history: list):
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/users/{st.session_state.local_id}/chats/{chat_name}"

    json_data = json.dumps(chat_history)

    body = {
        "fields": {
            "data": { "stringValue": json_data },
            "created_at": { "integerValue": int(time.time() * 1000) }
        }
    }

    r = firestore_request("PATCH", url, body)

    if 200 <= r.status_code < 300:
        st.session_state.toast = {
            "message": f"Successfully saved chat '{chat_name}'",
            "icon": ":material/check:"
        }
        st.session_state.load_chats = True
    else:
        st.session_state.toast = {
            "message": f"Failed to save chat '{chat_name}'",
            "icon": ":material/error:"
        }

# ---------------------------------------
# Delete chat from DB for current user
# ---------------------------------------
def delete_chat(chat_name: str):
    url = (
        f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
        f"/databases/(default)/documents/users/{st.session_state.local_id}/chats/{chat_name}"
    )

    r = firestore_request("DELETE", url)

    if 200 <= r.status_code < 300:
        st.session_state.toast = {
            "message": f"Successfully deleted chat '{chat_name}'",
            "icon": ":material/delete:"
        }
        st.session_state.load_chats = True
    else:
        st.session_state.toast = {
            "message": f"Failed to save chat '{chat_name}'",
            "icon": ":material/error:"
        }

# ---------------------------------------
# Load all chats from DB for current user
# ---------------------------------------
def load_chats():
    url = (
        f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
        f"/databases/(default)/documents/users/{st.session_state.local_id}/chats"
    )
    
    r = firestore_request("GET", url)

    if 200 <= r.status_code < 300:
        docs = r.json().get("documents", [])
        
        results = {}

        for doc in docs:
            chat_id = doc["name"].split("/")[-1]

            raw_json = doc["fields"].get("data", {}).get("stringValue", "[]")

            try:
                chat_list = json.loads(raw_json)
            except Exception:
                chat_list = []

            results[chat_id] = chat_list

        st.session_state.chat_histories = results

# ---------------------------------------
# Handle retry
# ---------------------------------------
def firestore_request(method, url, data=None):
    headers = {"Authorization": f"Bearer {st.session_state.id_token}"}
    r = requests.request(method, url, json=data, headers=headers)

    # If token expired, refresh & retry once
    if r.status_code == 401:
        refresh_id_token()
        headers = {"Authorization": f"Bearer {st.session_state.id_token}"}
        r = requests.request(method, url, json=data, headers=headers)

    return r

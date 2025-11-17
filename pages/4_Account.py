import streamlit as st
import time
from utils.sidebar import render_sidebar
from utils.initialize import initialize
from utils.constants import account_state
from services.authentication import authenticate
from services.database import delete_chat

# ---------------------------------------
# Initialize session
# ---------------------------------------
initialize()

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:
    render_sidebar(account_state)

# ---------------------------------------
# Clear inputs functions
# ---------------------------------------
def clear_login_fields():
    st.session_state.login_email_key = f"login_email_{time.time()}"
    st.session_state.login_password_key =  f"login_password_{time.time()}"
    st.rerun()

def clear_signup_fields():
    st.session_state.signup_email_key = f"signup_email_{time.time()}"
    st.session_state.signup_password_key =  f"signup_password_{time.time()}"
    st.rerun()

# ---------------------------------------
# Delete Saved Chat Dialog
# ---------------------------------------
@st.dialog("Delete Saved Chat")
def delete_chat_dialog(chat_name):
    st.write(f"Are you sure you want to delete '{chat_name}'?")

    if st.button("Delete", key="delete_chat_button", use_container_width=True):
        delete_chat(chat_name)
        st.rerun()

# ---------------------------------------
# Page Header
# ---------------------------------------
st.title('⚙️ Account')

# ---------------------------------------
# Unauthenticated Workflow
# ---------------------------------------
if any(st.session_state[key] is None for key in ("user", "id_token", "refresh_token", "local_id")):
    st.caption("🚀 Please **log in** or **sign up** to manage chat history.")
    login_tab, signup_tab = st.tabs(["🔑 Log In", "📝 Sign Up"])

    # LOGIN TAB
    with login_tab:
        st.subheader("Log In")

        email = st.text_input("📧 Email", key=st.session_state.login_email_key)
        password = st.text_input("🔐 Password", type="password", key=st.session_state.login_password_key)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Submit", use_container_width=True, key="login_button"):
                if email != "" and password != "":
                    authenticate(email, password, "signInWithPassword")
                    clear_login_fields()
                else:
                    st.toast("Input fields cannot be empty.", icon=":material/warning:")
        with col2:
            if st.button("Clear", use_container_width=True, key="login_clear_button"):
                clear_login_fields()

    # SIGNUP TAB
    with signup_tab:
        st.subheader("Sign Up")

        email = st.text_input("📧 Email", key=st.session_state.signup_email_key)
        password = st.text_input("🔐 Password", type="password", key=st.session_state.signup_password_key)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Submit", use_container_width=True, key="signup_button"):
                if email != "" and password != "":
                    authenticate(email, password, "signUp")
                    clear_signup_fields()
                else:
                    st.toast("Input fields cannot be empty.", icon=":material/warning:")
        
        with col2:
            if st.button("Clear", use_container_width=True, key="signup_clear_button"):
                clear_signup_fields()

# ---------------------------------------
# Authenticated Workflow
# ---------------------------------------
else:
    st.caption(f"🎉 You are logged in as **{st.session_state.user}**")
    st.subheader("💬 Your Saved Chats")

    histories = st.session_state.get("chat_histories", {})

    if not histories:
        st.info("No chat history saved yet.", icon=":material/info:")
    else:

        for chat_id, history in histories.items():
            col_expander, col_delete = st.columns([12, 1])

            with col_expander:
                with st.expander(f"🗂️ {chat_id}", expanded=False):
                    for msg in history:
                        st.chat_message(msg["role"]).markdown(msg["content"])

            with col_delete:
                if st.button(":material/delete:", key=f"delete_{chat_id}", help="Delete conversation", use_container_width=True):
                    delete_chat_dialog(chat_id)

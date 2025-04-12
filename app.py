# app.py
import streamlit as st
from caregiver_chatbot import CaregiverChatbot

st.set_page_config(page_title="Caregiver Support Chat", page_icon="💬")

# Initialize chatbot and session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = CaregiverChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👩‍⚕️ Caregiver Support Chatbot")

# Display chat history
for sender, message in st.session_state.messages:
    if sender == "user":
        st.markdown(f"<div style='text-align: right; background-color: #e0f7fa; padding: 10px; border-radius: 10px; margin: 5px 0;'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; background-color: #f1f8e9; padding: 10px; border-radius: 10px; margin: 5px 0;'><strong>Bot:</strong> {message}</div>", unsafe_allow_html=True)

# Text input with ENTER send
user_input = st.text_input("Type your message and press Enter...", key="input")
if user_input:
    st.session_state.messages.append(("user", user_input))
    bot_response = st.session_state.chatbot.process_message(user_input)
    st.session_state.messages.append(("bot", bot_response))
    st.experimental_rerun()

# Optional Quick Buttons
with st.expander("🔧 Quick Support Topics"):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💖 Emotional support"):
            st.session_state.messages.append(("user", "I feel overwhelmed"))
            response = st.session_state.chatbot.process_message("I feel overwhelmed")
            st.session_state.messages.append(("bot", response))
            st.experimental_rerun()
    with col2:
        if st.button("💊 Medication"):
            st.session_state.messages.append(("user", "I need help with medication"))
            response = st.session_state.chatbot.process_message("I need help with medication")
            st.session_state.messages.append(("bot", response))
            st.experimental_rerun()
    with col3:
        if st.button("📅 Appointment"):
            st.session_state.messages.append(("user", "Help me manage appointments"))
            response = st.session_state.chatbot.process_message("Help me manage appointments")
            st.session_state.messages.append(("bot", response))
            st.experimental_rerun()

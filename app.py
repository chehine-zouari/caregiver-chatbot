import streamlit as st
from caregiver_chatbot import CaregiverChatbot

# Init chatbot
if 'bot' not in st.session_state:
    st.session_state.bot = CaregiverChatbot()

st.title("👩‍⚕️ Caregiver Support Chatbot")
st.markdown("This assistant is here to support you emotionally and practically.")

# Chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Input from user
user_input = st.text_input("You:", placeholder="Tell me how you're feeling or ask a question...")

if user_input:
    response = st.session_state.bot.process_message(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

# Display chat
for speaker, msg in reversed(st.session_state.history):
    st.markdown(f"**{speaker}:** {msg}")

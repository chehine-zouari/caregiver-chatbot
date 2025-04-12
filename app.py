# app.py

class CaregiverChatbot:
    def process_message(self, message):
        message = message.lower()
        if "overwhelmed" in message or "tired" in message or "stress" in message:
            return "I'm really sorry you're feeling this way. Taking care of someone is incredibly challenging, and it's okay to feel overwhelmed."
        elif "medication" in message or "pill" in message:
            return "Let's talk about the medication. Do you have questions about dosage or timing?"
        elif "appointment" in message or "reminder" in message:
            return "Sure! Would you like me to help you set up an appointment reminder?"
        elif "lonely" in message:
            return "You're not alone. I'm here with you. Would talking to someone help right now?"
        else:
            return "You're doing great. How else can I support you today?"
            
import streamlit as st
from caregiver_chatbot import CaregiverChatbot

st.set_page_config(page_title="Caregiver AI Support", page_icon="🤖")

st.title("Caregiver Support Chatbot 🤖💬")

chatbot = CaregiverChatbot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = chatbot.process_message(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

st.markdown("#### Or select a quick support topic:")
if st.button("💖 Emotional support"):
    response = chatbot.process_message("I feel overwhelmed")
    st.session_state.chat_history.append(("You", "I feel overwhelmed"))
    st.session_state.chat_history.append(("Bot", response))

if st.button("💊 Medication help"):
    response = chatbot.process_message("I need help with medication")
    st.session_state.chat_history.append(("You", "I need help with medication"))
    st.session_state.chat_history.append(("Bot", response))

if st.button("📅 Appointment reminder"):
    response = chatbot.process_message("Help me manage appointments")
    st.session_state.chat_history.append(("You", "Help me manage appointments"))
    st.session_state.chat_history.append(("Bot", response))

for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")

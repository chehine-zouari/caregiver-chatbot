import streamlit as st
from PIL import Image
from caregiver_chatbot import CaregiverChatbot

# Branding and Page Configuration
logo = Image.open("your_logo.png")  # Make sure your logo image is in the same folder as your app
st.set_page_config(page_title="Digital Care Companion", page_icon="🧠")

# Layout for Logo and Title
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=100)
with col2:
    st.markdown("## 🧠 Digital Care Companion")
    st.markdown("**Empowering caregivers of children with medical complexity through AI.**")
    

st.set_page_config(page_title="Caregiver AI Support", page_icon="🤖")

st.title("Caregiver Support Chatbot 🤖💬")

# Allow the user to choose the tone before starting the conversation
tone_choice = st.selectbox("Choose your support style:", ["Soft", "Directive"])
chatbot = CaregiverChatbot(tone=tone_choice.lower())  # Set tone based on user's choice

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

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")

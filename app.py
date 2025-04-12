import streamlit as st
from PIL import Image
from caregiver_chatbot import CaregiverChatbot

# Set page configuration (Title and Icon)
st.set_page_config(page_title="Caregiver AI Support", page_icon="🤖")

# Load the logo image
try:
    logo = Image.open("Logo.jpg")  # Ensure the logo file is in the same folder as your app.py
except FileNotFoundError:
    st.error("Logo image not found. Please ensure 'Logo.jpg' is in the same directory.")
    logo = None  # Prevent further errors if the image is missing

# Display logo if it's loaded successfully
if logo:
    st.image(logo, width=100)

# Layout for Logo and Title
col1, col2 = st.columns([1, 5])
with col1:
    if logo:
        st.image(logo, width=100)  # Display logo again in the layout
with col2:
    st.markdown("## 🧠 Digital Care Companion")
    st.markdown("**Empowering caregivers of children with medical complexity through AI.**")

# Allow the user to choose the tone before starting the conversation
tone_choice = st.selectbox("Choose your support style:", ["Soft", "Directive"])

# Initialize the chatbot with the chosen tone
chatbot = CaregiverChatbot(tone=tone_choice.lower())

# Initialize chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input area
user_input = st.text_input("You:", "")

# Handling send button click
if st.button("Send"):
    if user_input:
        # Get the response from the chatbot
        response = chatbot.process_message(user_input)
        # Store the conversation in session state
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

# Provide quick support topic buttons
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

# Display the chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")

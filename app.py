import streamlit as st
from caregiver_chatbot import CaregiverChatbot

# Initialize the chatbot
chatbot = CaregiverChatbot()

# Title and instructions
st.title("Caregiver Support Chatbot")
st.write("""
    Welcome! I'm here to help with caregiving support. You can ask me for assistance with:
    - Medication schedules
    - Appointment reminders
    - Emotional support
    - Communication with healthcare providers
""")

# Create a text input field for the user to type their message
user_input = st.text_input("What can I assist you with today?")

# Display chatbot's response when user submits input
if user_input:
    response = chatbot.process_message(user_input)
    st.write(f"Bot: {response}")

# Display a feedback option for users
if user_input:
    feedback = st.text_input("How helpful was my response? Please provide feedback.")
    if feedback:
        st.write("Thank you for your feedback!")

import streamlit as st
from PIL import Image
from caregiver_chatbot import CaregiverChatbot
import pandas as pd
from datetime import datetime
from deep_translator import GoogleTranslator  # Use deep_translator for translation

# Set page configuration (Title and Icon)
st.set_page_config(page_title="Caregiver AI Support", page_icon="🤖")

# Load the logo image
try:
    logo = Image.open("Logo.jpg")  # Ensure the logo file is in the same folder as your app.py
except FileNotFoundError:
    st.error("Logo image not found. Please ensure 'Logo.jpg' is in the same directory.")
    logo = None  # Prevent further errors if the image is missing

# Layout for Logo and Title
col1, col2 = st.columns([1, 5])
with col1:
    if logo:
        st.image(logo, width=100)  # Display logo again in the layout
with col2:
    st.markdown("## 🤖 Digital Care Companion 🤖")
    st.markdown("**Empowering caregivers of children with medical complexity through AI.**")

# Language selection dropdown
language_choice = st.selectbox("Choose your language:", [
    "English", "Mandarin Chinese", "Hindi", "Spanish", "French", "Standard Arabic", "Bengali", "Portuguese", "Russian", "Urdu"
])

# Mapping languages to codes for translation
language_mapping = {
    "English": "en",
    "Mandarin Chinese": "zh",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Standard Arabic": "ar",
    "Bengali": "bn",
    "Portuguese": "pt",
    "Russian": "ru",
    "Urdu": "ur"
}

# Initialize chatbot with chosen language
chatbot = CaregiverChatbot(tone="soft")

# Initialize chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to translate messages
def translate_message(message, target_language):
    return GoogleTranslator(source='auto', target=target_language).translate(message)

# Function to translate the chatbot's response
def translate_response(response, target_language):
    return GoogleTranslator(source='auto', target=target_language).translate(response)

# User input area
user_input = st.text_input("You:", "")

# Handling send button click
if st.button("Send"):
    if user_input:
        # Translate user input to English before passing it to the chatbot
        translated_input = translate_message(user_input, 'en')
        
        # Get the response from the chatbot (in English)
        response = chatbot.process_message(translated_input)
        
        # Translate the chatbot's response back to the selected language
        translated_response = translate_response(response, language_mapping[language_choice])

        # Store the conversation in session state with timestamp
        st.session_state.chat_history.append(("You", user_input, datetime.now()))
        st.session_state.chat_history.append(("Bot", translated_response, datetime.now()))

# Provide quick support topic buttons
st.markdown("#### Or select a quick support topic:")
if st.button("💖 Emotional support"):
    response = chatbot.process_message("I feel overwhelmed")
    translated_response = translate_response(response, language_mapping[language_choice])
    st.session_state.chat_history.append(("You", "I feel overwhelmed", datetime.now()))
    st.session_state.chat_history.append(("Bot", translated_response, datetime.now()))

if st.button("💊 Medication help"):
    response = chatbot.process_message("I need help with medication")
    translated_response = translate_response(response, language_mapping[language_choice])
    st.session_state.chat_history.append(("You", "I need help with medication", datetime.now()))
    st.session_state.chat_history.append(("Bot", translated_response, datetime.now()))

if st.button("📅 Appointment reminder"):
    response = chatbot.process_message("Help me manage appointments")
    translated_response = translate_response(response, language_mapping[language_choice])
    st.session_state.chat_history.append(("You", "Help me manage appointments", datetime.now()))
    st.session_state.chat_history.append(("Bot", translated_response, datetime.now()))

# Helper: convert sentiment scores to DataFrame
def get_mood_df(history):
    timestamps = []
    scores = []

    for entry in history:
        if entry[0] == 'You' and len(entry) >= 3:
            timestamps.append(entry[2])
            scores.append(chatbot.analyze_sentiment(entry[1])['score'])

    # Optional: handle case where no valid entries are found
    if not timestamps or not scores:
        return pd.DataFrame({'Time': [], 'Mood Score': []})

    return pd.DataFrame({'Time': timestamps, 'Mood Score': scores})

# Mood Evolution Dashboard
if st.sidebar.checkbox("📈 Show Mood Evolution Dashboard"):
    df = get_mood_df(st.session_state.chat_history)
    if not df.empty:
        st.subheader("Caregiver Mood Evolution Over Time")
        st.line_chart(df.rename(columns={"Time": "index"}).set_index("index"))
        st.caption("This chart shows how the caregiver's emotional tone has changed over time based on their messages.")
    else:
        st.write("No conversation history to show mood evolution.")

# Care Tasks Tracker in Sidebar
st.sidebar.markdown("## 🩺 Care Tasks Tracker")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

task_type = st.sidebar.selectbox("Task Type", ["Medication", "Doctor Appointment", "Feeding", "Nap", "Other"])
task_name = st.sidebar.text_input("Task Description")
task_date = st.sidebar.date_input("Select Date")
task_time = st.sidebar.time_input("Select Time")

if st.sidebar.button("➕ Add Task"):
    if task_name:
        task = {
            "type": task_type,
            "name": task_name,
            "date": task_date.strftime("%Y-%m-%d"),
            "time": task_time.strftime("%H:%M")
        }
        st.session_state.tasks.append(task)
        st.sidebar.success("✅ Task added successfully!")
    else:
        st.sidebar.warning("Please enter a task description.")

# Display chat history
for entry in st.session_state.chat_history:
    speaker, message = entry[0], entry[1]
    st.markdown(f"**{speaker}:** {message}")

# Show care tasks if mentioned
if st.checkbox("📋 Show Care Tasks"):
    st.subheader("Scheduled Care Tasks")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            st.markdown(f"**{task['type']}** — {task['name']} at {task['time']} on {task['date']}")
    else:
        st.info("No tasks scheduled yet. Use the sidebar to add care activities.")

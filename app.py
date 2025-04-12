import streamlit as st
from PIL import Image
from caregiver_chatbot import CaregiverChatbot
import pandas as pd
import matplotlib.pyplot as plt

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

# Helper: convert sentiment scores to DataFrame
def get_mood_df(history):
    timestamps = [entry[1] for entry in history]  # User message timestamp
    scores = [chatbot.analyze_sentiment(entry[1])['score'] for entry in history if entry[0] == 'You']  # Get sentiment scores
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

# Display the chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")


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

for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")

# Show care tasks if mentioned
if st.checkbox("📋 Show Care Tasks"):
    st.subheader("Scheduled Care Tasks")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            st.markdown(f"**{task['type']}** — {task['name']} at {task['time']} on {task['date']}")
    else:
        st.info("No tasks scheduled yet. Use the sidebar to add care activities.")

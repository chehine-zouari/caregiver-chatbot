import streamlit as st
from PIL import Image
from caregiver_chatbot import CaregiverChatbot
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import base64

# Set page configuration (Title and Icon)
st.set_page_config(page_title="Caregiver AI Support", page_icon="🤖")

# Load the logo image
try:
    logo = Image.open("Logo.jpg")
except FileNotFoundError:
    st.error("Logo image not found. Please ensure 'Logo.jpg' is in the same directory.")
    logo = None

# Layout for Logo and Title
col1, col2 = st.columns([1, 5])
with col1:
    if logo:
        st.image(logo, width=100)
with col2:
    st.markdown("## 🤖 Digital Care Companion 🤖")
    st.markdown("**Empowering caregivers of children with medical complexity through AI.**")

# Tone selection
tone_choice = st.selectbox("Choose your support style:", ["Soft", "Directive"])
chatbot = CaregiverChatbot(tone=tone_choice.lower())

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", "")
if st.button("Send"):
    if user_input:
        response = chatbot.process_message(user_input)
        st.session_state.chat_history.append(("You", user_input, datetime.now()))
        st.session_state.chat_history.append(("Bot", response, datetime.now()))

# Quick buttons
st.markdown("#### Or select a quick support topic:")
quick_options = {
    "💖 Emotional support": "I feel overwhelmed",
    "💊 Medication help": "I need help with medication",
    "📅 Appointment reminder": "Help me manage appointments"
}
for label, prompt in quick_options.items():
    if st.button(label):
        response = chatbot.process_message(prompt)
        st.session_state.chat_history.append(("You", prompt, datetime.now()))
        st.session_state.chat_history.append(("Bot", response, datetime.now()))

# Mood tracking
def get_mood_df(history):
    timestamps, scores = [], []
    for entry in history:
        if entry[0] == 'You' and len(entry) >= 3:
            timestamps.append(entry[2])
            scores.append(chatbot.analyze_sentiment(entry[1])['score'])
    return pd.DataFrame({'Time': timestamps, 'Mood Score': scores}) if timestamps else pd.DataFrame({'Time': [], 'Mood Score': []})

if st.sidebar.checkbox("📈 Show Mood Evolution Dashboard"):
    df = get_mood_df(st.session_state.chat_history)
    if not df.empty:
        st.subheader("Caregiver Mood Evolution Over Time")
        st.line_chart(df.rename(columns={"Time": "index"}).set_index("index"))
        st.caption("Mood tracking powered by BERT-based sentiment analysis.")
    else:
        st.write("No conversation history to show mood evolution.")

# Care Tasks Tracker
st.sidebar.markdown("## 🦧 Care Tasks Tracker")
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

# Export chat history
if st.sidebar.button("⬇️ Export Chat History"):
    if st.session_state.chat_history:
        df_chat = pd.DataFrame(
            [(s, m, t.strftime("%Y-%m-%d %H:%M:%S")) for s, m, t in st.session_state.chat_history],
            columns=["Speaker", "Message", "Timestamp"]
        )
        csv = df_chat.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="chat_history.csv">📥 Download CSV</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
    else:
        st.sidebar.warning("No chat history available to export.")

# Chat history display
for speaker, message, *_ in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")

# Task display
if st.checkbox("📋 Show Care Tasks"):
    st.subheader("Scheduled Care Tasks")
    if st.session_state.tasks:
        for task in st.session_state.tasks:
            st.markdown(f"**{task['type']}** — {task['name']} at {task['time']} on {task['date']}")
    else:
        st.info("No tasks scheduled yet. Use the sidebar to add care activities.")

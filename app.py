import streamlit as st
import base64
import os
import streamlit.components.v1 as components
import random
import time

# ------------------ PAGE CONFIG -------------------
# This must be the very first Streamlit command
st.set_page_config(page_title="Caregiver AI Support", page_icon="🤖")

# ------------------ MAGIC BACKGROUND -------------------
def inject_custom_background():
   st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #e0f7fa, #e8eaf6, #f3e5f5, #e8f5e9);
        background-attachment: fixed;
    }
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #e8eaf6, #f3e5f5, #e8f5e9);
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

inject_custom_background()

# ------------------ MUSIC BACKGROUND -------------------

# 🎵 Music visualizer style
st.markdown("""
    <style>
    .audio-button {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
        gap: 6px;
        cursor: pointer;
    }
    .bar {
        width: 4px;
        height: 10px;
        background: #7e57c2;
        animation: wave 1.2s infinite ease-in-out;
    }
    .bar:nth-child(2) {
        animation-delay: -1.1s;
    }
    .bar:nth-child(3) {
        animation-delay: -1s;
    }
    .bar:nth-child(4) {
        animation-delay: -0.9s;
    }
    .bar:nth-child(5) {
        animation-delay: -0.8s;
    }
    @keyframes wave {
        0%, 100% {
            transform: scaleY(0.3);
        }
        50% {
            transform: scaleY(1);
        }
    }
    </style>
""", unsafe_allow_html=True)

# 🎶 Load and encode audio
def get_base64_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

audio_base64 = get_base64_audio("magical.mp4")

# 🎚 Session toggle
if "play_music" not in st.session_state:
    st.session_state.play_music = False

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔈 Play Music"):
        st.session_state.play_music = True
with col2:
    if st.button("🔇 Stop Music"):
        st.session_state.play_music = False

# 🔊 Embed music and animated visualizer if playing
if st.session_state.play_music:
    st.markdown(f"""
    <audio id="bgmusic" autoplay loop>
        <source src="data:audio/mp4;base64,{audio_base64}" type="audio/mp4">
    </audio>
    <div class="audio-button">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
    """, unsafe_allow_html=True)

# ------------------ HEADER AND CONTENT -------------------
from PIL import Image
from caregiver_chatbot import CaregiverChatbot
import pandas as pd
from datetime import datetime
import base64
from langdetect import detect
import torch  # Import torch to check if GPU is available

try:
    logo = Image.open("Logo.jpg")
except FileNotFoundError:
    st.error("Logo image not found. Please ensure 'Logo.jpg' is in the same directory.")
    logo = None

col1, col2 = st.columns([1, 5])
with col1:
    if logo:
        st.image(logo, width=100)
with col2:
    st.markdown("## 🤖 Digital Care Companion 🤖")
    st.markdown("**Empowering caregivers of children with medical complexity through AI.**")

language_choice = st.selectbox(
    "Choose your language:",
    ["English", "Mandarin Chinese", "Hindi", "Spanish", "French", "Standard Arabic", "Bengali", "Portuguese", "Russian", "Urdu"]
)

tone_choice = st.selectbox("Select chatbot tone:", ["Soft", "Directive"])

device = 0 if torch.cuda.is_available() else -1

chatbot = CaregiverChatbot(language=language_choice.lower(), device=device, tone=tone_choice.lower())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

if st.button("Send"):
    if user_input:
        detected_language = detect_language(user_input)
        chatbot.set_language(detected_language)
        response = chatbot.process_message(user_input)
        st.session_state.chat_history.append(("You", user_input, datetime.now()))
        st.session_state.chat_history.append(("Bot", response, datetime.now()))

st.markdown("#### Or select a quick support topic:")

if st.button("💖 Emotional support"):
    response = chatbot.process_message("I feel overwhelmed")
    st.session_state.chat_history.append(("You", "I feel overwhelmed", datetime.now()))
    st.session_state.chat_history.append(("Bot", response, datetime.now()))

if st.button("💊 Medication help"):
    response = chatbot.process_message("I need help with medication")
    st.session_state.chat_history.append(("You", "I need help with medication", datetime.now()))
    st.session_state.chat_history.append(("Bot", response, datetime.now()))

if st.button("📅 Appointment reminder"):
    response = chatbot.process_message("Help me manage appointments")
    st.session_state.chat_history.append(("You", "Help me manage appointments", datetime.now()))
    st.session_state.chat_history.append(("Bot", response, datetime.now()))

def get_mood_df(chat_history):
    moods = []
    scores = []
    for entry in chat_history:
        sentiment_result = chatbot.analyze_sentiment(entry[1])
        moods.append(sentiment_result['label'])
        scores.append(sentiment_result['score'])
    df = pd.DataFrame({"Mood": moods, "Score": scores})
    return df

if st.sidebar.checkbox("📈 Show Mood Evolution Dashboard"):
    df = get_mood_df(st.session_state.chat_history)
    if not df.empty:
        st.subheader("Caregiver Mood Evolution Over Time")
        if 'Time' in df.columns:
            df = df.rename(columns={"Time": "index"})
            st.line_chart(df.set_index("index"))
        else:
            st.line_chart(df)
        st.caption("This chart shows how the caregiver's emotional tone has changed over time based on their messages.")
    else:
        st.write("No conversation history to show mood evolution.")

st.sidebar.markdown("## 📋 Care Tasks Tracker")

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

if st.sidebar.button("⬇️ Export Chat History"):
    if st.session_state.chat_history:
        df_chat = pd.DataFrame(
            [(speaker, message, timestamp.strftime("%Y-%m-%d %H:%M:%S")) for speaker, message, timestamp in st.session_state.chat_history],
            columns=["Speaker", "Message", "Timestamp"]
        )
        csv = df_chat.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="chat_history.csv">📥 Download CSV</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
    else:
        st.sidebar.warning("No chat history available to export.")

for speaker, message, *_ in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")

if st.checkbox("📋 Show Care Tasks"):
    st.subheader("Scheduled Care Tasks")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            st.markdown(f"**{task['type']}** — {task['name']} at {task['time']} on {task['date']}")
    else:
        st.info("No tasks scheduled yet. Use the sidebar to add care activities.")




# Function to generate word search puzzle
def generate_word_search():
    words = ['care', 'love', 'peace', 'relax', 'calm']
    ws = WordSearch(words, size=10)
    return ws.generate()

# Fun affirmations
affirmations = [
    "You are doing great, keep it up!",
    "Remember to take a break, your health matters!",
    "You are strong and resilient!",
    "Take a deep breath and smile, you're doing amazing!",
]

# Streamlit UI
st.title("Caregiver Emotional Support Games")

# Options for games/activities
activity = st.selectbox("Choose an activity", ("Journaling", "Breathing Exercise", "Positive Affirmation"))

if activity == "Journaling":
    st.subheader("Journaling Activity")
    journal_entry = st.text_area("Write your thoughts here...", height=200)
    if journal_entry:
        st.write("Your thoughts today:")
        st.write(journal_entry)
    else:
        st.write("Take your time to reflect and write...")

elif activity == "Breathing Exercise":
    st.subheader("Breathing Exercise")
    breath_inhale = st.button("Inhale for 4 seconds")
    breath_hold = st.button("Hold for 7 seconds")
    breath_exhale = st.button("Exhale for 8 seconds")

    if breath_inhale:
        st.write("Inhale for 4 seconds...")
        time.sleep(4)
        st.write("Hold your breath...")
        time.sleep(7)
        st.write("Exhale slowly...")
        time.sleep(8)
        st.write("Repeat this a few times to calm your mind.")

elif activity == "Positive Affirmation":
    st.subheader("Get a Positive Affirmation")
    if st.button("Get Affirmation"):
        st.write(random.choice(affirmations))



# Initialize session state variables to track progress
if 'points' not in st.session_state:
    st.session_state.points = 0
    st.session_state.badges = []

# List of tasks
tasks = {
    "Caregiving Tasks": 10,  # 10 points for caregiving tasks
    "Wellness Activity": 5,   # 5 points for wellness activity
    "Daily Journal": 3,       # 3 points for journaling
}

# Function to add points and badges
def complete_task(task):
    st.session_state.points += tasks[task]
    st.session_state.badges.append(task)
    st.success(f"Task '{task}' completed! You've earned {tasks[task]} points.")

# Display tasks
st.title("Caregiver Progress Tracker")
st.subheader("Track your caregiving activities and earn rewards!")

for task, points in tasks.items():
    if st.button(f"Complete '{task}'"):
        complete_task(task)

# Display total points
st.subheader(f"Total Points: {st.session_state.points}")

# Display badges earned
if len(st.session_state.badges) > 0:
    st.subheader("Badges Earned:")
    for badge in st.session_state.badges:
        st.write(f"🏅 {badge}")
else:
    st.write("No badges earned yet. Start completing tasks!")

# Optional: Add a progress bar for a more visual representation
progress = (st.session_state.points / sum(tasks.values())) * 100
st.progress(progress)

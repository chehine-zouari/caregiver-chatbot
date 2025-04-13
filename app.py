import streamlit as st
import base64

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

# Function to load and encode the MP4
def load_audio_base64(file_path):
    with open(file_path, "rb") as f:
        audio_data = f.read()
    return base64.b64encode(audio_data).decode()

# Load audio file
encoded_music = load_audio_base64("magical.mp4")  # make sure this file exists

# Inject HTML audio tag with JS controller
audio_html = f"""
<audio id="bg-music" loop>
    <source src="data:audio/mp3;base64,{encoded_music}" type="audio/mp3">
</audio>

<script>
const audio = document.getElementById("bg-music");

function playAudio() {{
    audio.play();
}}

function pauseAudio() {{
    audio.pause();
}}
</script>
"""
st.markdown(audio_html, unsafe_allow_html=True)

# UI Buttons to control the music
col1, col2 = st.columns(2)
with col1:
    if st.button("🔊 Turn ON Music"):
        st.markdown('<script>playAudio();</script>', unsafe_allow_html=True)
with col2:
    if st.button("🔇 Turn OFF Music"):
        st.markdown('<script>pauseAudio();</script>', unsafe_allow_html=True)

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

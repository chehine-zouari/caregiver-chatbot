# app.py

def process_message(self, message):
    message = message.lower()
    
    if "overwhelmed" in message or "tired" in message or "stress" in message:
        return "😔 Hmm... that sounds really tough. Caregiving can be so exhausting sometimes. You're doing your best, and that's more than enough. I'm here for you 💛"
    
    elif "medication" in message or "pill" in message:
        return "💊 Got it. Medication can be tricky, right? Do you need help keeping track of doses or timing? I'm here to help you sort it out 👍"
    
    elif "appointment" in message or "reminder" in message:
        return "📅 Of course! I can help with that. Would you like me to set up a gentle reminder for upcoming appointments? 😊"
    
    elif "lonely" in message:
        return "💙 Ouch... loneliness is hard. Just know you’re not alone right now. I'm right here with you. Want to talk a little more? 🫂"

    elif "angry" in message or "frustrated" in message:
        return "😤 Ugh, I get that. It’s completely okay to feel frustrated. Want to vent a bit? I’m here to listen."

    elif "sad" in message or "cry" in message:
        return "😭 I’m so sorry you’re feeling this way. It’s okay to cry—it means you care deeply. Sending you a big virtual hug 🤗"

    elif "thank" in message:
        return "😊 Aww, you're very welcome! I'm really glad I could help 💖"

    elif "help" in message:
        return "🤝 Sure thing! Just tell me what you need and I’ll do my best to be useful."

    else:
        return "🫶 You're doing great, seriously. Being a caregiver isn’t easy. How else can I support you today?"
            
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

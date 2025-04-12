
import streamlit as st
from textblob import TextBlob
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import random

class CaregiverChatbot:
    def __init__(self):
        self.conversation_history = []
        self.sentiment_scores = []
        self.user_profile = {}
        
    def analyze_sentiment(self, text):
        # Basic sentiment analysis with TextBlob
        blob = TextBlob(text)
        score = blob.sentiment.polarity
        if score < -0.5:
            urgency = 'high'
            emotions = ['overwhelmed', 'distressed']
        elif score < 0:
            urgency = 'medium'
            emotions = ['concerned', 'anxious']
        else:
            urgency = 'low'
            emotions = ['hopeful', 'positive']
        return {'score': score, 'emotions': emotions, 'urgency': urgency}

    def save_interaction(self, user_input, response):
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'sentiment': self.analyze_sentiment(user_input)
        }
        self.conversation_history.append(interaction)

    def get_feedback(self):
        return "How helpful was my response? Your feedback helps me provide better support."

    def process_message(self, user_input):
        sentiment = self.analyze_sentiment(user_input)
        self.sentiment_scores.append(sentiment['score'])

        if "emotion" in user_input.lower():
            return "I understand this can be challenging. Please take a deep breath. You're doing great!"
        
        if "medication" in user_input.lower():
            return "Would you like me to help you manage the medication schedule?"
        
        return "I'm here to help! How can I assist you today?"

# Dashboard and caregiver mood tracking
def plot_mood_trend(sentiment_scores):
    df = pd.DataFrame(sentiment_scores, columns=['Score'])
    df['Time'] = pd.to_datetime(df.index, unit='s')
    st.line_chart(df.set_index('Time'))

# Initialize chatbot
chatbot = CaregiverChatbot()

# Streamlit UI components
st.title("Caregiver Chatbot")
st.subheader("Welcome! How can I assist you today?")
input_text = st.text_input("Enter your message:")

if input_text:
    response = chatbot.process_message(input_text)
    st.write(f"Bot: {response}")
    chatbot.save_interaction(input_text, response)

    # Plot mood trend
    plot_mood_trend(chatbot.sentiment_scores)

# Display conversation history (Optional feature)
if st.checkbox("Show conversation history"):
    st.write(chatbot.conversation_history)

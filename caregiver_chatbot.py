from textblob import TextBlob
from datetime import datetime

class CaregiverChatbot:
    def __init__(self):
        self.conversation_history = []
        self.sentiment_scores = []

    def analyze_sentiment(self, text):
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

        return {
            'score': score,
            'emotions': emotions,
            'urgency': urgency
        }

    def detect_burnout_signs(self, recent_sentiments):
        if len(recent_sentiments) >= 5:
            negative_count = sum(1 for s in recent_sentiments if s < -0.3)
            if negative_count >= 3:
                return True
        return False

    def determine_response_type(self, text, medical_terms, emotional_terms):
        text = text.lower()
        if any(term in text for term in medical_terms):
            return 'medical'
        elif any(term in text for term in emotional_terms):
            return 'emotional'
        return 'general'

    def generate_response(self, user_input):
        sentiment = self.analyze_sentiment(user_input)
        self.sentiment_scores.append(sentiment['score'])

        medical_keywords = ['medication', 'doctor', 'appointment', 'symptoms']
        emotional_keywords = ['stressed', 'tired', 'overwhelmed', 'worried']

        response_type = self.determine_response_type(user_input, medical_keywords, emotional_keywords)

        if response_type == 'medical':
            return self.generate_medical_response(user_input)
        elif response_type == 'emotional':
            return self.generate_emotional_support(sentiment)
        else:
            return self.generate_general_response()

    def generate_medical_response(self, query):
        responses = {
            'medication': "Would you like help managing the medication schedule?",
            'appointment': "I can help you keep track of appointments.",
            'symptoms': "Let me help you document these symptoms for your doctor."
        }

        for key in responses:
            if key in query.lower():
                return responses[key]
        return "How can I assist you with medical care today?"

    def generate_emotional_support(self, sentiment):
        if sentiment['score'] < -0.5:
            return ("I hear you're having a tough time. "
                    "Want to talk or would you prefer practical help?")
        elif sentiment['score'] < 0:
            return ("I understand this is challenging. "
                    "Remember to take breaks and care for yourself too.")
        else:
            return "You're doing great. How else can I support you today?"

    def generate_general_response(self):
        return ("I'm here to help! Would you like assistance with:\n"
                "- Medication schedules\n"
                "- Appointment reminders\n"
                "- Emotional support\n"
                "- Communication with doctors")

    def process_message(self, user_input):
        response = self.generate_response(user_input)

        if self.detect_burnout_signs(self.sentiment_scores[-5:]):
            response += ("\n\nI notice you've been overwhelmed lately. "
                         "Would you like some support resources?")
        return response

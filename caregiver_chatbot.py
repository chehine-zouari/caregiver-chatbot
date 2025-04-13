from textblob import TextBlob
class CaregiverChatbot:
    def __init__(self, tone="soft"):
        self.tone = tone  # Can be 'soft' or 'directive'

    def set_tone(self, tone):
        if tone in ["soft", "directive"]:
            self.tone = tone

    def analyze_sentiment(self, message):
        """Analyze the sentiment of the given message."""
        blob = TextBlob(message)  # Create a TextBlob object for sentiment analysis
        sentiment_score = blob.sentiment.polarity  # Get sentiment polarity (-1 to 1)
        return {"score": sentiment_score}

    def process_message(self, message):
        message = message.lower()

        if self.tone == "soft":
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
            elif "task" in message or "what are my care tasks" in message or "show tasks" in message:
                return "📋 Here are your scheduled care tasks. Please check the section below."
            else:
                return "🫶 You're doing great, seriously. Being a caregiver isn’t easy. How else can I support you today?"

        elif self.tone == "directive":
            if "overwhelmed" in message or "tired" in message or "stress" in message:
                return "💡 Let's take a breath. Start by listing your top 3 priorities. Together, we can find a way to manage this better."
            elif "medication" in message or "pill" in message:
                return "📋 Let’s make a simple schedule for medication tracking. Do you want a reminder every day or just weekly?"
            elif "appointment" in message or "reminder" in message:
                return "✅ Let’s organize your upcoming appointments. You can create a digital note or calendar entry — I’ll guide you if needed."
            elif "lonely" in message:
                return "🤝 Feeling lonely is valid. I suggest reaching out to a support group or friend. Would you like a resource link?"
            elif "angry" in message or "frustrated" in message:
                return "⚠️ Anger is a signal. Let’s channel that into action — maybe write down what triggered it and how to prevent it."
            elif "sad" in message or "cry" in message:
                return "📘 When sadness hits, journaling or a short walk can help. Want me to suggest a reflection prompt?"
            elif "thank" in message:
                return "✅ I’m always ready to assist. Let’s keep going strong!"
            elif "help" in message:
                return "🚀 Just let me know what task or challenge you're dealing with — and we’ll tackle it step by step."
            elif "task" in message or "what are my care tasks" in message or "show tasks" in message:
                return "📋 Here are your scheduled care tasks. Please check the section below."
            else:
                return "🛠️ What would you like to work on next? You’ve got this — and I’ve got your back."



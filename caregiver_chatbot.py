from transformers import pipeline

class CaregiverChatbot:
    def __init__(self, tone="soft"):
        self.tone = tone  # Can be 'soft' or 'directive'
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    def set_tone(self, tone):
        if tone in ["soft", "directive"]:
            self.tone = tone

    def analyze_sentiment(self, message):
        """Analyze the sentiment using BERT."""
        result = self.sentiment_analyzer(message)[0]
        label = result['label']  # e.g., '4 stars'
        score = int(label[0])  # Convert to int (1 to 5)
        normalized_score = (score - 3) / 2  # Normalize to -1 (bad) to +1 (good)
        return {"score": normalized_score, "label": label}

    def detect_keywords(self, message, keywords):
        return any(keyword in message.lower() for keyword in keywords)

    def process_message(self, message):
        message = message.lower()

        emotion_keywords = {
            "overwhelmed": ["overwhelmed", "tired", "stress"],
            "medication": ["medication", "pill"],
            "appointment": ["appointment", "reminder"],
            "lonely": ["lonely"],
            "angry": ["angry", "frustrated"],
            "sad": ["sad", "cry"],
            "thank": ["thank"],
            "help": ["help"],
            "task": ["task", "what are my care tasks", "show tasks"]
        }

        for emotion, keywords in emotion_keywords.items():
            if self.detect_keywords(message, keywords):
                return self._generate_response(emotion)

        return self._generate_response("default")

    def _generate_response(self, emotion):
        soft_responses = {
            "overwhelmed": "😔 Hmm... that sounds really tough. Caregiving can be so exhausting sometimes. You're doing your best, and that's more than enough. I'm here for you 💛",
            "medication": "💊 Got it. Medication can be tricky, right? Do you need help keeping track of doses or timing? I'm here to help you sort it out 👍",
            "appointment": "📅 Of course! I can help with that. Would you like me to set up a gentle reminder for upcoming appointments? 😊",
            "lonely": "💙 Ouch... loneliness is hard. Just know you’re not alone right now. I'm right here with you. Want to talk a little more? 🫂",
            "angry": "😤 Ugh, I get that. It’s completely okay to feel frustrated. Want to vent a bit? I’m here to listen.",
            "sad": "😭 I’m so sorry you’re feeling this way. It’s okay to cry—it means you care deeply. Sending you a big virtual hug 🤗",
            "thank": "😊 Aww, you're very welcome! I'm really glad I could help 💖",
            "help": "🤝 Sure thing! Just tell me what you need and I’ll do my best to be useful.",
            "task": "📋 Here are your scheduled care tasks. Please check the section below.",
            "default": "🫶 You're doing great, seriously. Being a caregiver isn’t easy. How else can I support you today?"
        }

        directive_responses = {
            "overwhelmed": "💡 Let's take a breath. Start by listing your top 3 priorities. Together, we can find a way to manage this better.",
            "medication": "📋 Let’s make a simple schedule for medication tracking. Do you want a reminder every day or just weekly?",
            "appointment": "✅ Let’s organize your upcoming appointments. You can create a digital note or calendar entry — I’ll guide you if needed.",
            "lonely": "🤝 Feeling lonely is valid. I suggest reaching out to a support group or friend. Would you like a resource link?",
            "angry": "⚠️ Anger is a signal. Let’s channel that into action — maybe write down what triggered it and how to prevent it.",
            "sad": "📘 When sadness hits, journaling or a short walk can help. Want me to suggest a reflection prompt?",
            "thank": "✅ I’m always ready to assist. Let’s keep going strong!",
            "help": "🚀 Just let me know what task or challenge you're dealing with — and we’ll tackle it step by step.",
            "task": "📋 Here are your scheduled care tasks. Please check the section below.",
            "default": "🛠️ What would you like to work on next? You’ve got this — and I’ve got your back."
        }

        return soft_responses[emotion] if self.tone == "soft" else directive_responses[emotion]

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch


class CaregiverChatbot:
    def __init__(self, language="en", device=None, tone="soft"):
        """
        Initializes the CaregiverChatbot with a language, device, and tone.

        :param language: str, default "en" - language preference (currently placeholder)
        :param device: int or None - device ID for GPU (-1 for CPU, None for auto)
        :param tone: str - either 'soft' or 'directive'
        """
        self.language = language
        self.device = device if device is not None else (0 if torch.cuda.is_available() else -1)
        self.tone = tone

        try:
            model_name = "gpt2"
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model.to(f"cuda:{self.device}" if self.device >= 0 else "cpu")
        except Exception as e:
            print(f"[Error] Model initialization failed: {e}")
            self.model = None
            self.tokenizer = None

        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis", device=self.device)
        except Exception as e:
            print(f"[Warning] Sentiment analysis pipeline initialization failed: {e}")
            self.sentiment_analyzer = None

    def set_language(self, language):
        """
        Change chatbot's language preference (currently symbolic).
        """
        self.language = language
        print(f"[Info] Language changed to: {language}")
        # Language adaptation for multilingual models can be added here.

    def analyze_sentiment(self, message):
        """
        Analyze the sentiment of a message using Hugging Face pipeline.

        :param message: str
        :return: dict with sentiment label and score
        """
        if not self.sentiment_analyzer:
            return {"label": "UNKNOWN", "score": 0.0}

        try:
            result = self.sentiment_analyzer(message)
            sentiment = result[0]['label']
            score = result[0]['score']
            return {"label": sentiment, "score": score}
        except Exception as e:
            print(f"[Error] Sentiment analysis failed: {e}")
            return {"label": "UNKNOWN", "score": 0.0}

    def process_message(self, message):
        """
        Processes the user message and returns a chatbot response based on tone.

        :param message: str
        :return: str response
        """
        message_lower = message.lower()

        # Keywords grouped by category
        emotions = {
            "overwhelmed": ["overwhelmed", "tired", "stress"],
            "medication": ["medication", "pill"],
            "appointment": ["appointment", "reminder"],
            "lonely": ["lonely"],
            "angry": ["angry", "frustrated"],
            "sad": ["sad", "cry"],
            "thanks": ["thank"],
            "help": ["help"],
            "tasks": ["task", "what are my care tasks", "show tasks"]
        }

        # Helper to match keyword
        def matches(category):
            return any(keyword in message_lower for keyword in emotions[category])

        if self.tone == "soft":
            if matches("overwhelmed"):
                return "😔 Hmm... that sounds really tough. Caregiving can be so exhausting sometimes. You're doing your best, and that's more than enough. I'm here for you 💛"
            elif matches("medication"):
                return "💊 Got it. Medication can be tricky, right? Do you need help keeping track of doses or timing? I'm here to help you sort it out 👍"
            elif matches("appointment"):
                return "📅 Of course! I can help with that. Would you like me to set up a gentle reminder for upcoming appointments? 😊"
            elif matches("lonely"):
                return "💙 Ouch... loneliness is hard. Just know you’re not alone right now. I'm right here with you. Want to talk a little more? 🫂"
            elif matches("angry"):
                return "😤 Ugh, I get that. It’s completely okay to feel frustrated. Want to vent a bit? I’m here to listen."
            elif matches("sad"):
                return "😭 I’m so sorry you’re feeling this way. It’s okay to cry—it means you care deeply. Sending you a big virtual hug 🤗"
            elif matches("thanks"):
                return "😊 Aww, you're very welcome! I'm really glad I could help 💖"
            elif matches("help"):
                return "🤝 Sure thing! Just tell me what you need and I’ll do my best to be useful."
            elif matches("tasks"):
                return "📋 Here are your scheduled care tasks. Please check the section below."
            else:
                return "🫶 You're doing great, seriously. Being a caregiver isn’t easy. How else can I support you today?"

        elif self.tone == "directive":
            if matches("overwhelmed"):
                return "💡 Let's take a breath. Start by listing your top 3 priorities. Together, we can find a way to manage this better."
            elif matches("medication"):
                return "📋 Let’s make a simple schedule for medication tracking. Do you want a reminder every day or just weekly?"
            elif matches("appointment"):
                return "✅ Let’s organize your upcoming appointments. You can create a digital note or calendar entry — I’ll guide you if needed."
            elif matches("lonely"):
                return "🤝 Feeling lonely is valid. I suggest reaching out to a support group or friend. Would you like a resource link?"
            elif matches("angry"):
                return "⚠️ Anger is a signal. Let’s channel that into action — maybe write down what triggered it and how to prevent it."
            elif matches("sad"):
                return "📘 When sadness hits, journaling or a short walk can help. Want me to suggest a reflection prompt?"
            elif matches("thanks"):
                return "✅ I’m always ready to assist. Let’s keep going strong!"
            elif matches("help"):
                return "🚀 Just let me know what task or challenge you're dealing with — and we’ll tackle it step by step."
            elif matches("tasks"):
                return "📋 Here are your scheduled care tasks. Please check the section below."
            else:
                return "🛠️ What would you like to work on next? You’ve got this — and I’ve got your back."

        else:
            return "⚠️ Sorry, I don’t recognize that tone. Please set the tone to either 'soft' or 'directive'."


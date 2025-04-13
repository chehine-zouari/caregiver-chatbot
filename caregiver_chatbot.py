from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class CaregiverChatbot:
    def __init__(self, language="en", device=-1, tone="soft"):
        self.language = language
        self.device = device
        self.tone = tone

        # Initialize the model and tokenizer
        try:
            model_name = "gpt2"  # Change to your model's name if needed
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model.to(self.device)
        except Exception as e:
            print(f"Error initializing the chatbot: {e}")

        # Initialize sentiment analysis pipeline from HuggingFace
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def analyze_sentiment(self, message):
        """
        Analyze sentiment of the input message (positive/negative)
        :param message: Input message text
        :return: sentiment label ('POSITIVE' or 'NEGATIVE') and score (confidence)
        """
        try:
            sentiment_result = self.sentiment_analyzer(message)
            # Ensure the result is consistent and return it in a structured way
            sentiment = sentiment_result[0]['label'] if sentiment_result else "NEUTRAL"
            score = sentiment_result[0]['score'] if sentiment_result else 0.0
            return {"label": sentiment, "score": score}
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {"label": "NEUTRAL", "score": 0.0}  # Return neutral in case of error

    def process_message(self, message):
        """
        Process the incoming message based on the selected tone (soft or directive)
        :param message: Input message text
        :return: Response based on the tone
        """
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

# Example of how this class might be used
if __name__ == "__main__":
    chatbot = CaregiverChatbot(language="en", tone="soft")

    # Example message to process and analyze sentiment
    message = "I'm feeling anxious"
    sentiment = chatbot.analyze_sentiment(message)
    print(f"Sentiment: {sentiment['label']}, Score: {sentiment['score']}")

    # Example response based on tone
    response = chatbot.process_message(message)
    print(f"Response: {response}")

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from langdetect import detect
import openai
import logging

openai.api_key = 'your-openai-api-key'

class CaregiverChatbot:
    def __init__(self, language="en", device=-1):
        self.language = language
        self.device = device
        self.model, self.tokenizer = self.load_model(language)

    def load_model(self, language):
        try:
            model_name = f"Helsinki-NLP/opus-mt-en-{language}" if language != 'en' else "t5-base"
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            return model, tokenizer
        except Exception as e:
            logging.error(f"Failed to load model for language {language}: {e}")
            raise ValueError("Model loading failed")

    def process_message(self, message):
        try:
            inputs = self.tokenizer(message, return_tensors="pt", padding=True, truncation=True).to(self.device)
            output = self.model.generate(**inputs)
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            return response
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            return "Sorry, I couldn't understand that."

    def analyze_sentiment(self, message):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Analyze the sentiment of this message: '{message}'",
                max_tokens=60
            )
            sentiment_score = response.choices[0].text.strip()
            return {"score": sentiment_score}
        except Exception as e:
            logging.error(f"Error analyzing sentiment: {e}")
            return {"score": 0}

    def set_language(self, language):
        self.language = language
        self.model, self.tokenizer = self.load_model(language)

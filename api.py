from flask import Flask, request, jsonify
from src.chatbot import Chatbot
from src.sentiment import SentimentAnalyzer
from src.summary import ConversationSummarizer
from src.utils import load_environment_variables
import os

app = Flask(__name__)

# Initialize components
load_environment_variables()
chatbot = None
sentiment_analyzer = None
summarizer = None

try:
    chatbot = Chatbot()
    sentiment_analyzer = SentimentAnalyzer()
    summarizer = ConversationSummarizer(chatbot)
    print("All components initialized successfully")
except Exception as e:
    print(f"Error initializing components: {str(e)}")

@app.route('/api/chat', methods=['POST'])
def chat():
    if not chatbot:
        return jsonify({'error': 'Chatbot not initialized'}), 500
    
    data = request.json
    user_message = data.get('message')
    history = data.get('history', [])
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
        
    try:
        response = chatbot.get_response(user_message, history)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    if not sentiment_analyzer:
        return jsonify({'error': 'Sentiment analyzer not initialized'}), 500
        
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
        
    try:
        result = sentiment_analyzer.analyze_statement(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emotion', methods=['POST'])
def analyze_emotion():
    if not sentiment_analyzer:
        return jsonify({'error': 'Sentiment analyzer not initialized'}), 500
        
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
        
    try:
        result = sentiment_analyzer.analyze_emotion(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summary', methods=['POST'])
def generate_summary():
    if not summarizer:
        return jsonify({'error': 'Summarizer not initialized'}), 500
        
    data = request.json
    history = data.get('history')
    
    if not history:
        return jsonify({'error': 'History is required'}), 400
        
    try:
        # Basic summary without sentiment/emotion results for simplicity in this API
        # In a real scenario, we might want to pass those if available or compute them
        summary = summarizer.generate_ai_summary(history)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

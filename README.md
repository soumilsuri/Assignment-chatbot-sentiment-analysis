# Chatbot with Sentiment Analysis

A sophisticated chatbot application that conducts conversations with users and performs sentiment analysis on the entire conversation. Built with Google Gemini API for intelligent responses and Hugging Face transformers for sentiment analysis.

## Features

### Tier 1 - Mandatory Requirements ✅

- **Full Conversation History**: Maintains complete conversation context throughout the interaction
- **Conversation-Level Sentiment Analysis**: Analyzes the entire conversation and provides overall emotional direction
- **Clear Sentiment Output**: Displays sentiment with formatted output: "Overall conversation sentiment: [Label] – [Description]"
- **Interactive Chat Interface**: Clean, modern UI built with Streamlit

### Tier 2 - Additional Credit ✅ IMPLEMENTED

- **Statement-Level Sentiment Analysis**: Analyzes each user message individually with sentiment labels and confidence scores
- **Real-Time Sentiment Display**: Shows sentiment badges next to each message as it's sent (toggleable)
- **Multi-Dimensional Emotion Analysis**: Uses `j-hartmann/emotion-english-distilroberta-base` to detect:
  - Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral
  - Emotion radar chart visualization
  - Emotion intensity tracking
- **Mood Trend Visualization**: 
  - Interactive line charts showing sentiment progression over time
  - Emotion intensity trends
  - Sentiment distribution charts
- **Conversation Summary**: 
  - Automatic conversation summarization
  - Mood trajectory description
  - Key emotional moments extraction
- **Dual Analysis Modes**: Toggle between basic sentiment analysis and comprehensive emotion analysis

## Technology Stack

### Core Technologies

- **Python 3.8+**: Primary programming language
- **Streamlit**: Web framework for building the interactive UI
- **Google Gemini API**: Powers the chatbot's conversational intelligence
- **Hugging Face Transformers**: Provides sentiment analysis capabilities
- **PyTorch**: Deep learning framework for model inference

### Libraries & Dependencies

- `streamlit`: Modern web app framework for Python
- `google-generativeai`: Official Google Gemini API client
- `transformers`: Hugging Face library for NLP models
- `torch`: PyTorch for model inference
- `python-dotenv`: Environment variable management
- `pandas`: Data handling utilities
- `plotly`: Interactive data visualization for charts and graphs

## Project Structure

```
Assignment-chatbot-sentiment-analysis/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── chatbot.py           # Gemini API integration
│   ├── sentiment.py         # Sentiment & emotion analysis module
│   ├── conversation.py      # Conversation history management
│   ├── visualization.py    # Chart and graph generation
│   ├── summary.py          # Conversation summarization
│   └── utils.py             # Utility functions
├── app.py                   # Streamlit main application
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Assignment-chatbot-sentiment-analysis
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   # Copy the example file
   # On Windows (PowerShell)
   Copy-Item .env.example .env
   
   # On macOS/Linux
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```
   
   The application will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Start a Conversation**
   - Type your message in the chat input at the bottom
   - Press Enter or click Send
   - The chatbot will respond using Gemini AI

2. **Continue the Conversation**
   - Keep chatting! The bot maintains full conversation history
   - All messages are displayed in the chat interface

3. **Analyze Sentiment/Emotion**
   - Choose analysis mode: "Basic Sentiment" or "Emotion Analysis" in the sidebar
   - Click the "📊 Analyze Sentiment" or "📊 Analyze Emotion" button
   - The system will analyze the entire conversation
   - Results will show:
     - Overall sentiment/emotion
     - Interactive visualizations (trend charts, radar charts)
     - Statement-level analysis for each message
     - Conversation summary and mood trajectory
     - Key emotional moments

4. **Real-Time Analysis**
   - Toggle "Show real-time sentiment badges" in the sidebar
   - Sentiment and emotion badges will appear next to each user message as you type
   - Colors indicate sentiment/emotion type

5. **Clear Conversation**
   - Click "🗑️ Clear Conversation" in the sidebar to start fresh

## Sentiment Analysis Logic

### Model Used

The application uses **`cardiffnlp/twitter-roberta-base-sentiment-latest`**, a RoBERTa-based model fine-tuned on Twitter data for sentiment analysis. This model is:
- Lightweight and efficient
- Trained specifically for social media and conversational text
- Provides three-class sentiment classification (Negative, Neutral, Positive)

### Analysis Process

1. **Text Preparation**: Only **user messages** are analyzed for sentiment, as sentiment analysis reflects the user's emotional state and satisfaction level. The chatbot's responses are excluded since they don't represent user sentiment.

2. **Tokenization**: The user messages are concatenated and tokenized using the model's tokenizer with:
   - Maximum length: 512 tokens (handles most conversations)
   - Truncation for longer conversations
   - Proper padding for batch processing

3. **Inference**: 
   - The model processes the tokenized input
   - Softmax activation provides probability scores for each sentiment class
   - The highest confidence label is selected

4. **Output Formatting**:
   - Primary label: Negative, Neutral, or Positive
   - Confidence score: Probability of the selected label
   - Explanation: Contextual description based on confidence level
   - Formatted output: "Overall conversation sentiment: [Label] – [Explanation]"

### Sentiment Interpretation

- **Positive**: Indicates satisfaction, positive engagement, or favorable interaction
- **Negative**: Indicates dissatisfaction, concerns, complaints, or negative feedback
- **Neutral**: Indicates balanced, mixed, or neither strongly positive nor negative sentiment

The confidence score helps assess the strength of the sentiment classification. Higher confidence (>70%) indicates stronger sentiment, while lower confidence suggests more ambiguous sentiment.

## Code Architecture

### Modular Design

The codebase follows a modular, production-ready structure:

- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Error Handling**: Comprehensive error handling for API calls and model loading
- **Environment Management**: Secure API key handling via environment variables
- **Session Management**: Proper state management in Streamlit for conversation persistence

### Key Components

1. **`ConversationManager`**: Handles conversation history, message formatting, and state management
2. **`Chatbot`**: Manages Gemini API integration and response generation
3. **`SentimentAnalyzer`**: Loads and runs the sentiment analysis model
4. **`app.py`**: Streamlit UI that orchestrates all components

## Status of Tier 2 Implementation

**Current Status**: ✅ **FULLY IMPLEMENTED**

All Tier 2 features have been successfully implemented:

- ✅ **Statement-Level Sentiment Analysis**: Each user message is analyzed individually
- ✅ **Real-Time Sentiment Display**: Sentiment badges appear next to messages (toggleable in sidebar)
- ✅ **Multi-Dimensional Emotion Analysis**: Full emotion detection with 7 emotion categories
- ✅ **Emotion Radar Chart**: Visual representation of emotion distribution
- ✅ **Mood Trend Visualization**: Interactive charts showing sentiment/emotion progression
- ✅ **Conversation Summary**: Automatic summarization with mood trajectory
- ✅ **Key Emotional Moments**: Extraction of high-intensity emotional moments
- ✅ **Dual Analysis Modes**: Switch between basic sentiment and comprehensive emotion analysis

## Testing

To test the application:

1. Start a conversation with various sentiment expressions
2. Try positive messages: "I love this service!", "Great job!"
3. Try negative messages: "This is terrible", "I'm disappointed"
4. Try mixed conversations to see how overall sentiment is calculated
5. Use the sentiment analysis button to verify results

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `.env` file exists in the root directory
   - Verify `GEMINI_API_KEY` is set correctly
   - Check that the API key is valid and has proper permissions

2. **Model Loading Issues**
   - First run will download the model (~500MB) - ensure stable internet connection
   - Model is cached after first download
   - If download fails, try running again

3. **Import Errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

4. **Streamlit Not Starting**
   - Check if port 8501 is available
   - Try: `streamlit run app.py --server.port 8502`

## Future Enhancements

- [x] Tier 2: Statement-level sentiment analysis ✅
- [x] Real-time sentiment indicators per message ✅
- [x] Mood trend visualization with charts ✅
- [x] Conversation summarization ✅
- [ ] Conversation export functionality
- [ ] Multiple sentiment model options
- [ ] Multi-language support
- [ ] Custom emotion categories
- [ ] Sentiment/emotion history tracking across sessions

## License

This project is created for educational/assignment purposes.

## Author

Developed as part of the LiaPlus Assignment - Chatbot with Sentiment Analysis.

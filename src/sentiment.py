"""
Sentiment analysis module using Hugging Face transformers.
Includes basic sentiment and multi-dimensional emotion analysis.
"""

from typing import Dict, List, Tuple, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


class SentimentAnalyzer:
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest", 
                 emotion_model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        self.model_name = model_name
        self.emotion_model_name = emotion_model_name
        self.tokenizer = None
        self.model = None
        self.emotion_tokenizer = None
        self.emotion_model = None
        self.labels = ['negative', 'neutral', 'positive']
        self.emotion_labels = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'neutral']
        self._load_models()
    
    def _load_models(self):
        try:
            print(f"Loading sentiment model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.eval()
            print("Sentiment model loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load sentiment model: {str(e)}")
        
        try:
            print(f"Loading emotion model: {self.emotion_model_name}")
            self.emotion_tokenizer = AutoTokenizer.from_pretrained(self.emotion_model_name)
            self.emotion_model = AutoModelForSequenceClassification.from_pretrained(self.emotion_model_name)
            self.emotion_model.eval()
            
            try:
                if hasattr(self.emotion_model.config, 'id2label') and self.emotion_model.config.id2label:
                    id2label = self.emotion_model.config.id2label
                    self.emotion_labels = [id2label[i].lower() for i in sorted(id2label.keys())]
                elif hasattr(self.emotion_model.config, 'label2id') and self.emotion_model.config.label2id:
                    label2id = self.emotion_model.config.label2id
                    self.emotion_labels = [label.lower() for label in sorted(label2id.keys(), key=lambda x: label2id[x])]
            except Exception:
                pass
            
            print(f"Emotion model loaded successfully with labels: {self.emotion_labels}")
        except Exception as e:
            print(f"Warning: Failed to load emotion model: {str(e)}")
            self.emotion_tokenizer = None
            self.emotion_model = None
    
    def analyze(self, text: str) -> Dict[str, any]:
        if not text or not text.strip():
            return {
                'label': 'neutral',
                'confidence': 0.0,
                'scores': {'negative': 0.33, 'neutral': 0.34, 'positive': 0.33}
            }
        
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        scores = predictions[0].tolist()
        score_dict = {label: float(score) for label, score in zip(self.labels, scores)}
        
        max_idx = scores.index(max(scores))
        label = self.labels[max_idx]
        confidence = float(scores[max_idx])
        sentiment_score = self._calculate_sentiment_score(label, confidence, score_dict)
        
        return {
            'label': label,
            'confidence': confidence,
            'scores': score_dict,
            'score': sentiment_score
        }
    
    def analyze_conversation(self, conversation_text: str) -> Dict[str, any]:
        result = self.analyze(conversation_text)
        explanation = self._generate_explanation(result)
        formatted_output = f"Overall conversation sentiment: {result['label'].capitalize()} – {explanation}"
        
        return {
            **result,
            'explanation': explanation,
            'formatted_output': formatted_output,
            'score': result.get('score', 50)
        }
    
    def _generate_explanation(self, result: Dict[str, any]) -> str:
        label = result['label']
        confidence = result['confidence']
        
        explanations = {
            'positive': [
                'general satisfaction and positive engagement',
                'overall positive interaction',
                'favorable conversation tone',
                'positive user experience'
            ],
            'negative': [
                'general dissatisfaction',
                'overall negative interaction',
                'unfavorable conversation tone',
                'user concerns or complaints'
            ],
            'neutral': [
                'neutral or balanced interaction',
                'mixed or neutral conversation tone',
                'neither strongly positive nor negative'
            ]
        }
        
        # Select explanation based on confidence
        if confidence > 0.7:
            explanation = explanations[label][0]
        elif confidence > 0.5:
            explanation = explanations[label][1]
        else:
            explanation = explanations[label][2] if len(explanations[label]) > 2 else explanations[label][0]
        
        return explanation
    
    def _calculate_sentiment_score(self, label: str, confidence: float, scores: Dict[str, float]) -> int:
        if label == 'positive':
            # Positive: 50-100, weighted by confidence
            base_score = 50 + (scores['positive'] * 50)
            return int(base_score)
        elif label == 'negative':
            # Negative: 0-50, weighted by confidence
            base_score = 50 - (scores['negative'] * 50)
            return int(base_score)
        else:  # neutral
            # Neutral: around 40-60, centered at 50
            base_score = 50 + ((scores['positive'] - scores['negative']) * 10)
            return int(max(0, min(100, base_score)))
    
    def analyze_statement(self, text: str) -> Dict[str, any]:
        return self.analyze(text)
    
    def analyze_all_statements(self, messages: List[str]) -> List[Dict[str, any]]:
        results = []
        for msg in messages:
            result = self.analyze_statement(msg)
            results.append(result)
        return results
    
    def analyze_emotion(self, text: str) -> Dict[str, any]:
        if not self.emotion_model or not self.emotion_tokenizer:
            return {
                'label': 'neutral',
                'confidence': 0.0,
                'scores': {emotion: 0.0 for emotion in self.emotion_labels}
            }
        
        if not text or not text.strip():
            return {
                'label': 'neutral',
                'confidence': 0.0,
                'scores': {emotion: 0.14 for emotion in self.emotion_labels}
            }
        
        inputs = self.emotion_tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        
        with torch.no_grad():
            outputs = self.emotion_model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        scores = predictions[0].tolist()
        score_dict = {label: float(score) for label, score in zip(self.emotion_labels, scores)}
        
        max_idx = scores.index(max(scores))
        label = self.emotion_labels[max_idx]
        confidence = float(scores[max_idx])
        
        return {
            'label': label,
            'confidence': confidence,
            'scores': score_dict
        }
    
    def analyze_emotions_all_statements(self, messages: List[str]) -> List[Dict[str, any]]:
        results = []
        for msg in messages:
            result = self.analyze_emotion(msg)
            results.append(result)
        return results
    
    def get_emotion_summary(self, emotion_results: List[Dict[str, any]]) -> Dict[str, float]:
        if not emotion_results:
            return {emotion: 0.0 for emotion in self.emotion_labels}
        
        # Aggregate scores
        aggregated = {emotion: 0.0 for emotion in self.emotion_labels}
        for result in emotion_results:
            for emotion, score in result['scores'].items():
                aggregated[emotion] += score
        
        # Average
        count = len(emotion_results)
        return {emotion: score / count for emotion, score in aggregated.items()}


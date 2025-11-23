"""
Visualization module for sentiment and emotion analysis.
"""

import plotly.graph_objects as go
from typing import List, Dict, Optional


def create_emotion_radar_chart(emotion_scores: Dict[str, float]) -> go.Figure:
    emotions = list(emotion_scores.keys())
    scores = list(emotion_scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=emotions,
        fill='toself',
        name='Emotion Distribution',
        line=dict(color='rgb(99, 110, 250)')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Emotion Distribution Across Conversation",
        font=dict(size=12)
    )
    
    return fig


def create_mood_trend_chart(sentiment_results: List[Dict[str, any]], 
                            emotion_results: Optional[List[Dict[str, any]]] = None) -> go.Figure:
    message_indices = list(range(1, len(sentiment_results) + 1))
    
    sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    sentiment_values = [sentiment_map.get(result['label'], 0) * result['confidence'] 
                       for result in sentiment_results]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=message_indices,
        y=sentiment_values,
        mode='lines+markers',
        name='Sentiment Trend',
        line=dict(color='rgb(99, 110, 250)', width=3),
        marker=dict(size=8)
    ))
    
    if emotion_results:
        emotion_intensities = [result['confidence'] for result in emotion_results]
        fig.add_trace(go.Scatter(
            x=message_indices,
            y=emotion_intensities,
            mode='lines+markers',
            name='Emotion Intensity',
            line=dict(color='rgb(239, 85, 59)', width=2, dash='dash'),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Mood Trend Over Conversation",
        xaxis_title="Message Number",
        yaxis_title="Sentiment Score / Emotion Intensity",
        hovermode='x unified',
        font=dict(size=12)
    )
    
    return fig


def create_sentiment_distribution_chart(sentiment_results: List[Dict[str, any]]) -> go.Figure:
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for result in sentiment_results:
        label = result['label']
        if label in sentiment_counts:
            sentiment_counts[label] += 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sentiment_counts.keys()),
            y=list(sentiment_counts.values()),
            marker_color=['green', 'gray', 'red'],
            text=list(sentiment_counts.values()),
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Sentiment Distribution",
        xaxis_title="Sentiment",
        yaxis_title="Count",
        font=dict(size=12)
    )
    
    return fig


def get_sentiment_color(label: str) -> str:
    colors = {
        'positive': '#22c55e',
        'negative': '#ef4444',
        'neutral': '#eab308'
    }
    return colors.get(label, '#6b7280')


def get_emotion_color(emotion: str) -> str:
    colors = {
        'joy': '#fbbf24',
        'sadness': '#3b82f6',
        'anger': '#ef4444',
        'fear': '#8b5cf6',
        'surprise': '#ec4899',
        'disgust': '#10b981',
        'neutral': '#6b7280'
    }
    return colors.get(emotion, '#6b7280')


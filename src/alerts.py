"""
Sentiment threshold alert system.
Monitors sentiment and triggers alerts when thresholds are crossed.
"""

from typing import Dict, List, Optional, Callable
from datetime import datetime


class SentimentAlertManager:
    def __init__(self, threshold: float = 30.0, alert_callback: Optional[Callable] = None):
        self.threshold = threshold
        self.alert_callback = alert_callback
        self.alert_history: List[Dict[str, any]] = []
        self.alert_enabled = True
    
    def check_sentiment(self, sentiment_score: float, message: Optional[str] = None) -> Optional[Dict[str, any]]:
        if not self.alert_enabled:
            return None
        
        if sentiment_score < self.threshold:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'score': sentiment_score,
                'threshold': self.threshold,
                'message': message,
                'severity': self._calculate_severity(sentiment_score)
            }
            
            self.alert_history.append(alert)
            
            if self.alert_callback:
                self.alert_callback(alert)
            
            return alert
        
        return None
    
    def check_statement_sentiment(self, sentiment_result: Dict[str, any], 
                                 message: Optional[str] = None) -> Optional[Dict[str, any]]:
        score = sentiment_result.get('score', 50)
        return self.check_sentiment(score, message)
    
    def _calculate_severity(self, score: float) -> str:
        if score < 10:
            return 'critical'
        elif score < 20:
            return 'high'
        elif score < 30:
            return 'medium'
        else:
            return 'low'
    
    def set_threshold(self, threshold: float):
        if 0 <= threshold <= 100:
            self.threshold = threshold
    
    def enable_alerts(self):
        self.alert_enabled = True
    
    def disable_alerts(self):
        self.alert_enabled = False
    
    def get_alert_history(self) -> List[Dict[str, any]]:
        return self.alert_history.copy()
    
    def clear_alerts(self):
        self.alert_history = []


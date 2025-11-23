import unittest
import json
from api import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_sentiment_analysis(self):
        response = self.app.post('/api/sentiment', 
                                 data=json.dumps({'text': 'I am very happy today!'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['label'], 'positive')

    def test_emotion_analysis(self):
        response = self.app.post('/api/emotion', 
                                 data=json.dumps({'text': 'I am furious about this!'}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['label'], 'anger')

    def test_chat_endpoint(self):
        # Mocking might be needed for real external calls, but for integration test we can try a simple call
        # Assuming the API key is set and valid
        response = self.app.post('/api/chat', 
                                 data=json.dumps({'message': 'Hello', 'history': []}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)

    def test_summary_endpoint(self):
        history = [
            {'role': 'user', 'content': 'Hi'},
            {'role': 'assistant', 'content': 'Hello! How can I help?'},
            {'role': 'user', 'content': 'I am testing the summary.'}
        ]
        response = self.app.post('/api/summary', 
                                 data=json.dumps({'history': history}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('summary', data)

if __name__ == '__main__':
    unittest.main()

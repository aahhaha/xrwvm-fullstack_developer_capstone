from flask import Flask, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.get('/')
def home():
    return jsonify(service='sentiment', status='healthy')

@app.get('/analyze/<path:text>')
def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    sentiment = 'positive' if scores['compound'] >= .05 else 'negative' if scores['compound'] <= -.05 else 'neutral'
    return jsonify(sentiment=sentiment, scores=scores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

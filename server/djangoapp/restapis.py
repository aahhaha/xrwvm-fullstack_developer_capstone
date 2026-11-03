import os
import requests
from urllib.parse import quote

backend_url = os.environ.get('backend_url', 'http://localhost:3030').rstrip('/')
sentiment_analyzer_url = os.environ.get('sentiment_analyzer_url', 'http://localhost:5050').rstrip('/')

def get_request(endpoint, **kwargs):
    response = requests.get(backend_url + '/' + endpoint.lstrip('/'), params=kwargs, timeout=15)
    response.raise_for_status()
    return response.json()

def analyze_review_sentiments(text):
    response = requests.get(sentiment_analyzer_url + '/analyze/' + quote(text, safe=''), timeout=15)
    response.raise_for_status()
    return response.json()

def post_review(data_dict):
    response = requests.post(backend_url + '/insert_review', json=data_dict, timeout=15)
    response.raise_for_status()
    return response.json()

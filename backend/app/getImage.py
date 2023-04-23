import os
import sys
import random
import requests
from dotenv import load_dotenv

# Fetch an image from Google Custom Search API
def get_image(query):
    load_dotenv()
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        print("GOOGLE_API_KEY not found in .env file")
        sys.exit(1)
    pse_id = '86382df91391748a6'
    params = {
        'cx': pse_id,
        'num': '10',
        'q': query,
        'searchType': 'image',
        'key': key
    }
    response = requests.get(
        'https://www.googleapis.com/customsearch/v1', params=params)
    data = response.json()
    res = random.choice(data['items'])
    return res['link']
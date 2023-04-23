import random
import requests

def get_image(query):
    google_key = 'AIzaSyC1vWrV1Fkdiu1vEQMc_cuxb6kSI13Q-i4'
    pse_id = '86382df91391748a6'
    params = {
        'cx': pse_id,
        'num': '10',
        'q': query,
        'searchType': 'image',
        'key': google_key
    }
    response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
    data = response.json()
    res = random.choice(data['items'])
    return res['link']
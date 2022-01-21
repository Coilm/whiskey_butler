from joblib import Parallel, delayed
import requests
import re
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import os

from dotenv import load_dotenv
load_dotenv()
token = os.environ.get("api-token")

def extract_review_from_url(url):
    try:
        CLIENT_ID = os.environ.get("CLIENT_ID")
        PASSWORD_ID = os.environ.get("PASSWORD_ID")
        USERNAME= os.environ.get("USERNAME")
        PASSWORD = os.environ.get("PASSWORD")
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, PASSWORD_ID)

        data = {'grant_type': 'password',
                'username': USERNAME,
                'password': PASSWORD}

        headers = {'User-Agent': 'MyBot/0.0.1'}

        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)

        TOKEN = res.json()['access_token']

        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        if type(url) == str:
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'https://' + url
            url = re.sub(url.split('://')[1].split('/')[0], 'oauth.reddit.com', url)
            if url[-1] == '/':
                url += '?sort=old'
            else:
                url += '/?sort=old'

        response = requests.get(url, headers=headers)
        response = response.json()

        data = response[0]['data']['children'][0]['data']['selftext'].replace('\n', ' ')
        if data == '':  # If the main post is empty, then take the first comment
            data = response[1]['data']['children'][0]['data']['body'].replace('\n', ' ')

    except:
        data = ''

    return data



def convert_float_na(x):
    try:
        return float(x)
    except:
        return np.nan

df_reddit_raw = pd.read_csv('Reddit Whisky Network Review Archive - Review Archive.csv')

df_reddit_raw['Whisky Name'] = df_reddit_raw['Whisky Name'].str.strip()
df_reddit_raw['Reviewer Rating'] = df_reddit_raw['Reviewer Rating'].apply(lambda x: convert_float_na(x))

urls = list(df_reddit_raw['Link To Reddit Review'])

parallel_results = Parallel(n_jobs=-1)(delayed(extract_review_from_url)(urls[i]) for i in tqdm(range(len(urls))))

with open("review_results.txt", 'w') as f:
    json.dump(parallel_results, f)
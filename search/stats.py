from requests import get, post
from sys import exit
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()


HOST = 'https://api.chartmetric.com'
TOKEN = os.getenv("CHARTMETRIC_KEY")

res = post(f'{HOST}/api/token', json={"refreshtoken": TOKEN})
if res.status_code != 200:
    print(f'ERROR: received a {res.status_code} instead of 200 from /api/token')
    exit(1)

access_token = res.json()['token']
def Get(uri):
    return get(f'{HOST}{uri}', headers={'Authorization': f'Bearer {access_token}'})

res = Get('/api/artist/206557')
if res.status_code != 200:
    print(f'ERROR: received a {res.status_code} instead of 200 from /api/artist/:id')
    exit(1)

pprint(res.json())
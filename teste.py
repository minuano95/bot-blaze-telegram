import requests
import json

response = requests.get('https://blaze.com/api/roulette_games/recent')
response = json.loads(response.text)
print(response)
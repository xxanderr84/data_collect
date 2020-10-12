import requests
import json

main_link = "https://api.github.com/users/"
user = "xxanderr84"
response = requests.get(main_link + user + "/repos")
j_data = response.json()

with open('repository.json', 'w') as f:
    json.dump(j_data, f)


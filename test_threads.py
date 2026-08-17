import requests

from config import THREADS_ACCESS_TOKEN


url = "https://graph.threads.net/v1.0/me"

response = requests.get(
    url,
    params={
        "fields": "id,username",
        "access_token": THREADS_ACCESS_TOKEN,
    },
    timeout=30,
)

print(response.status_code)
print(response.text)
import requests

# 변수 설정
client_secret = "a8e35989ad3470d9afbf9a7237e5813f"
short_lived_token = "THAAQpFFIqARVBUVRhUWR4VXF5Rkx6OHJmZAE9wNmg1bjRpM3AxUW5lTk9pazVFLUhRVTBJR2lhdUx1aGc1c2hxc3lYZAWtadGJ2ZAGF5NUtkQWtnUDQ1cTg2aFltbGc2LXhlYjFkUS1wZAUZAvNUdQTlMtZA3pTUXZAUbS1aUUE5blJFeUtwWXh6N0p4TzRQeDhINHRvNV9LbERrWXVfSjFaVEdmSHlfZAHEZD"

url = "https://graph.threads.net/access_token"
params = {
    "grant_type": "th_exchange_token",
    "client_secret": client_secret,
    "access_token": short_lived_token
}

response = requests.get(url, params=params)
data = response.json()
print(data)
import requests

def check_phone(phone):
    api_key = "a91656ca677750712f33739121b5aefc"
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone}"
    r = requests.get(url)
    return r.json()

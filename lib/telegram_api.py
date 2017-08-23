import requests
from secret_token import token
from urllib.parse import quote

def getMe():
    url = "https://api.telegram.org/%s/getMe" % token
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.read().decode('utf-8'))
    else:
        return None
    return data

def get_updates(offset=0):
    url = "https://api.telegram.org/%s/getUpdates?offset=%s" % (token, str(offset))
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

def send_message(text, user):
    url = "https://api.telegram.org/%s/sendMessage?chat_id=" % token + str(user) + "&parse_mode=HTML&text="
    url += quote(text)
    response = urllib.request.urlopen(url)
    try:
        data = json.loads(response.read())
        return data
    except:
        pass

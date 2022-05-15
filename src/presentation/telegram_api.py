import requests
import urllib.parse
from utils.constants import BOT_TOKEN, CHAT_ID

def send_message(msg):
    encoded_msg = urllib.parse.quote(msg)
    uri = f"https://api.telegram.org/{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={encoded_msg}"
    requests.post(uri, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'})

def send_message_to_dev(msg):
    encoded_msg = urllib.parse.quote(msg)
    uri = f"https://api.telegram.org/{BOT_TOKEN}/sendMessage?chat_id=800208858&text={encoded_msg}"
    requests.post(uri, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'})

def send_document(file_path):
    url = "https://api.telegram.org/{BOT_TOKEN}/sendDocument";
    files = {'document': open(file_path, 'rb')}
    data = {'chat_id' : f"{CHAT_ID}"}
    requests.post(url, files=files, data=data)
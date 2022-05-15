import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

NOVADATA_TOKEN=os.getenv('NOVADATA_TOKEN')
APPUNTAMENTI_TOKEN = os.getenv('APPUNTAMENTI_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

in_corso_di_query = urllib.parse.quote("in corso di")
appuntamenti_url = f'https://api.mementodatabase.com/v1/libraries/OijjARjVs/entries?token={APPUNTAMENTI_TOKEN}'
novadata_url = f'https://api.mementodatabase.com/v1/libraries/3QdNYo4Bc/search?q={in_corso_di_query}&fields=1,5,6,11,14,16,17,18,20,99,138,153&token={NOVADATA_TOKEN}'

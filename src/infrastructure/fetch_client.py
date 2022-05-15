import requests
from typing import Dict, List, Union, NewType
from utils.utility import logger
import time

Json_type = NewType('Json_type', str)
class FetchClient:
    def __init__(self):
        self.entries: Union[List, List[Dict]] = []

    def __get_data_from_api(self, url: str) -> Dict:
        try:
            response = requests.get(url)
            return response.json()
        except:
            print("Errore nella richiesta")
            logger.exception("Errore nella richiesta")
            return {}

    def fetch_data(self, url: str) -> None:
        json_data = self.__get_data_from_api(url)
        self.entries += json_data.get('entries') or []
        next_page_token = json_data.get('nextPageToken')

        while next_page_token:
            time.sleep(1)
            json_data = self.__get_data_from_api(url + '&pageToken=' + next_page_token)
            next_page_token = json_data.get('nextPageToken')
            self.entries += json_data['entries']

    def post_data(self, url: str, data: Json_type) -> None:
        try:
            headers = {'Content-type': 'application/json'}
            requests.post(url, data=data, headers=headers)
        except:
            logger.exception("Errore nella post")
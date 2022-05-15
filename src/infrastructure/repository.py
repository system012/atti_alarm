from typing import Dict
import json
from utils.utility import logger
from utils.utility import get_actual_path

def read() -> Dict:
    '''Reads json file and returns dict'''
    try:
        with open(get_actual_path('atti_alarm.json'), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except json.decoder.JSONDecodeError as no_value:
        print(f"Errore nella lettura del file {no_value}")
        logger.exception("Errore nella lettura del file")
        return {}

def write(data: Dict) -> None:
    '''Deletes json content and then writes dict to json file'''
    try:
        with open(get_actual_path('atti_alarm.json'), 'w', encoding='utf-8') as f:
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=6)
    except json.decoder.JSONDecodeError as error_write:
        print(f"Errore nella scrittura del file: {error_write}")
        logger.exception("Errore nella scrittura del file")
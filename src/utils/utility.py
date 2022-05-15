import logging
import datetime
from typing import Dict
from os import path

def get_actual_path(*args: str) -> str: #nome del file e la sua estensione, es: report.html
    '''Returns path of current working directory'''
    actual_path_to_script = path.dirname(path.realpath(path.join(__file__, '..')))
    return path.join(actual_path_to_script, *args)


def filter_atti_by_attivita(atti: Dict, attivita: str) -> Dict:
    '''Filters atti by attivita, such as Notifica and Esecuzione'''
    return {key: value for key, value in atti.items() if value.get('attivita').startswith(attivita)}

def reorder_atti_by_date(atti: Dict, date_type='data_scadenza') -> Dict:
    '''Reorders atti by date. Eg. data_scadenza, which is by default'''
    return dict(sorted(atti.items(), key=lambda x: datetime.datetime.strptime(x[1][date_type], '%d/%m').date()))

logging.basicConfig(filename=f"{get_actual_path('atti_log.log')}",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

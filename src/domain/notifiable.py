import json
import datetime
from typing import Dict
from domain import Atto
from utils.utility import logger

class Notificabile():
    def __init__(self, obj: dict) -> None:
        self.id_pex = obj.get('id_pex')
        self.atto = obj.get('atto')
        self.motivo_scadenza = obj.get('motivo_scadenza')
        self.attivita = obj.get('attivita')
        self.data_avviso = datetime.datetime.strptime(obj.get('data_avviso'), '%Y-%m-%d').date() if obj.get('data_avviso') else datetime.date.today()
        self.numero_avvisi = obj.get('numero_avvisi') or 0
        self.data_scadenza = obj.get('data_scadenza')
        self.formatted_data_scadenza = None # data_scadenza formatted to dd/mm
        self.data_allarme = None # data_scadenza formatted to isoformat
        self.validate_date()

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Notificabile):
            return False

        return self.id_pex == __o.id_pex
    
    def __dict__(self) -> Dict:
        return {self.id_pex: {'id_pex': self.id_pex, 'atto': self.atto, 'motivo_scadenza': self.motivo_scadenza, 'data_scadenza': self.formatted_data_scadenza, 'data_allarme': self.data_allarme, 'attivita': self.attivita, 'data_avviso': self.data_avviso.strftime('%Y-%m-%d'), 'numero_avvisi': self.numero_avvisi}}

    def validate_date(self):
        if self.data_scadenza is None:
            logger.error(f"Data scadenza non valida per atto: {self.id_pex}")

        elif isinstance(self.data_scadenza, str):
            self.data_scadenza = datetime.datetime.strptime(self.data_scadenza+'/2022', "%d/%m/%Y") # la data viene letta dal json, ed è una stringa in formato %d/%m, a cui bisogna aggiungere l'anno
            self.formatted_data_scadenza = self.data_scadenza.strftime('%d/%m')
            self.data_allarme = self.data_scadenza.isoformat()+'Z'

        elif isinstance(self.data_scadenza, datetime.date):
            self.formatted_data_scadenza = self.data_scadenza.strftime('%d/%m')
            self.data_allarme = datetime.datetime.strptime(self.data_scadenza.strftime('%Y-%m-%d'), '%Y-%m-%d').isoformat()+'Z' # converting to string and then back to a datetime.date object so that we can transform it to isoformat (compatible with memento)

    def get_data_avviso(self) -> datetime.date:
        return self.data_avviso

    def set_data_avviso(self, date: datetime.date) -> None:
        self.data_avviso = date
    
    def get_numero_avvisi(self) -> int:
        return self.numero_avvisi

    def increase_numero_avvisi(self, num: int):
        self.numero_avvisi += num

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def to_dict(self) -> Dict:
        return self.__dict__()

    @staticmethod
    def from_atto(atto_giudiziario: Atto) -> 'Notificabile':
        id_pex = atto_giudiziario.id_pex
        atto = atto_giudiziario.atto
        motivo_scadenza = atto_giudiziario.motivo_scadenza
        attivita = atto_giudiziario.attivita
        data_scadenza = atto_giudiziario.data_scadenza

        return Notificabile({'id_pex': id_pex, 'atto': atto, 'motivo_scadenza': motivo_scadenza, 'data_scadenza': data_scadenza, 'attivita': attivita})

    def is_notifiable(self, atti_avvisati: int) -> bool:
        '''Un atto è notificabile in presenza di almeno una condizione:
           1) ci sono nuovi atti da avvisare, anche se è già stato notificato ieri
           2) caso particolare: l'atto è stato notificato ieri con la versione settimanale che attribuisce numero_avvisi=0. In questo caso, anche se l'atto è stato notificato ieri, è notificabile oggi
           3) oppure, è stato avvisato due giorni fa a prescindere che ci siano nuovi atti da avvisare'''

        if atti_avvisati > 0:
            return True
        
        if self.numero_avvisi == 0:
            return True

        date_difference = datetime.date.today() - self.data_avviso
        is_notificabile_dopo_due_giorni = date_difference.days >= 2

        return is_notificabile_dopo_due_giorni
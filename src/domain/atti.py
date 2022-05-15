import datetime
import re
from typing import Union

class Atto:
    def __init__(self, atto_obj: dict) -> None:
        self.stato = atto_obj.get('Stato').get('value')
        self.modalita = atto_obj.get('Modalità').get('value')
        self.attivita = atto_obj.get('Attività').get('value')
        self.atto = atto_obj.get('Atto').get('value')
        self.id_pex = str(atto_obj.get('ID_PEX').get('value'))
        self.richiesta_del = self.date_addition(self.date_parser(atto_obj.get('Richiesta_del').get('value')), 1) if atto_obj.get('Richiesta_del') else datetime.date.today()  # aggiungo 1 giorno perché memento restituisce sempre una data indietro di un giorno
        self.tipologia = atto_obj.get('Tipologia').get('value')
        self.allarme = atto_obj.get('Allarme').get('value')
        self.stato_desiderato = self.stato.startswith('In corso di') or self.stato.startswith('In itinere')
        self.delta_num_of_days_for_state = 25
        self.delta_num_of_days_for_urgency = 7
        self.date_to_which_to_compare = datetime.date.today()
        self.motivo_scadenza = None
        self.data_scadenza = None
        self.motivo_scadenza_deposito = "Deposito"
        self.motivo_scadenza_urgente_o_oggi = "Urgente/Oggi"
        self.motivo_scadenza_citazione = "Citazione"
        self.motivo_scandeza_esecuzione = "Esecuzione"
    
    def date_parser(self, date: str) -> datetime.date:
        try:
            string_date = re.search(r'\d{4}-\d{2}-\d{2}', date).group()
            return datetime.datetime.strptime(string_date, '%Y-%m-%d').date()
        except:
            return None

    def date_addition(self, date: Union[datetime.date, None], num_of_days_to_add: int) -> datetime.date:
        if not date:
            return None
        self.data_scadenza = date + datetime.timedelta(days=num_of_days_to_add)
        return self.data_scadenza

    def date_subtraction(self, date: Union[datetime.date, None], num_of_days_to_detract: int) -> datetime.date:
        if not date:
            return None
        self.data_scadenza = date - datetime.timedelta(days=num_of_days_to_detract)
        return self.data_scadenza

    def is_expiring_by_state(self) -> bool:
        return self.stato_desiderato and self.date_addition(self.richiesta_del, self.delta_num_of_days_for_state) <= self.date_to_which_to_compare

    def is_expiring_by_urgency(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.modalita in ['OGGI', 'URGENTE'] and self.date_addition(self.richiesta_del, self.delta_num_of_days_for_urgency) <= self.date_to_which_to_compare
    
    def is_expiring(self, date_to_which_to_compare: datetime.date) -> bool:
        self.date_to_which_to_compare = date_to_which_to_compare
        self.motivo_scadenza = self.motivo_scadenza_deposito if self.is_expiring_by_state() else self.motivo_scadenza_urgente_o_oggi if self.is_expiring_by_urgency() else 'Nessun avviso'
        return self.is_expiring_by_state() or self.is_expiring_by_urgency()
    
    def __str__(self) -> str:
        return f"{self.id_pex}"

class Notifica(Atto):
    '''Classe base notifica'''

class NotificaTerminiImerese(Notifica):
    def __init__(self, data_obj):
        self.dal_giorno = self.date_addition(self.date_parser(data_obj.get('Dal_giorno').get('value')), 1) if data_obj.get('Dal_giorno') else datetime.date.today()
        super().__init__(data_obj)
    
    def is_expiring_by_state(self) -> bool:
        return self.stato_desiderato and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_state) <= self.date_to_which_to_compare

    def is_expiring_by_urgency(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.modalita in ['OGGI', 'URGENTE'] and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_urgency) <= self.date_to_which_to_compare

class NotificaConCitazione(Notifica): # esecuzione con citazione è un doppione, riscrivi
    def __init__(self, data_obj) -> None:
        self.data_citazione = self.date_addition(self.date_parser(data_obj.get(
            'Data_citazione').get('value')), 1) if data_obj.get('Data_citazione') else datetime.date.today()
        super().__init__(data_obj)

    def is_expiring_by_citation_date(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.date_subtraction(self.data_citazione, 5) <= self.date_to_which_to_compare

    def is_expiring(self, date_to_which_to_compare: datetime.date) -> bool:
        self.date_to_which_to_compare = date_to_which_to_compare
        self.motivo_scadenza = self.motivo_scadenza_deposito if self.is_expiring_by_state() else self.motivo_scadenza_urgente_o_oggi if self.is_expiring_by_urgency() else self.motivo_scadenza_citazione if self.is_expiring_by_citation_date() else 'Nessun avviso'
        return self.is_expiring_by_state() or self.is_expiring_by_urgency() or self.is_expiring_by_citation_date()
class Notifica_SR(Notifica):
    def __init__(self, notifica_obj):
        super().__init__(notifica_obj)
        self.code_pex_del = self.date_addition(self.date_parser(notifica_obj.get('Cod_PEX_del').get('value')), 1) if notifica_obj.get('Cod_PEX_del') else datetime.date.today()
        self.stato_desiderato = 'In gestione'

    def is_exempt(self) -> bool:
        return self.tipologia != '- Pagamento' and self.tipologia != 'Penale'

    def is_expiring_if_exempt(self) -> bool:
        return self.stato == self.stato_desiderato and self.allarme == 'Avvisami' and self.date_addition(self.code_pex_del, 10) <= self.date_to_which_to_compare

    def is_expiring(self, date_to_which_to_compare: datetime.date) -> bool:
        self.date_to_which_to_compare = date_to_which_to_compare
        self.motivo_scadenza = self.motivo_scadenza_deposito if self.is_expiring_by_state() else self.motivo_scadenza_urgente_o_oggi if self.is_expiring_by_urgency() else 'Nessun avviso'

        if self.is_exempt():
            return self.is_expiring_if_exempt()
        
        self.stato_desiderato = 'In corso di notifica' # cosa accade qui? dovrebbe acquisire nuovamente il valore originario di stato_desiderato dalla classe Atto
        return self.is_expiring_by_state() or self.is_expiring_by_urgency()

class Esecuzione(Atto):
    '''Classe base esecuzione'''

class EsecuzioneConCitazione(Esecuzione):
    def __init__(self, data_obj) -> None:
        self.data_citazione = self.date_addition(self.date_parser(data_obj.get(
            'Data_citazione').get('value')), 1) if data_obj.get('Data_citazione') else datetime.date.today()
        super().__init__(data_obj)

    def is_expiring_by_citation_date(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.date_subtraction(self.data_citazione, 5) <= self.date_to_which_to_compare

    def is_expiring(self, date_to_which_to_compare: datetime.date) -> bool:
        self.date_to_which_to_compare = date_to_which_to_compare
        self.motivo_scadenza = self.motivo_scadenza_deposito if self.is_expiring_by_state() else self.motivo_scadenza_urgente_o_oggi if self.is_expiring_by_urgency() else self.motivo_scadenza_citazione if self.is_expiring_by_citation_date() else 'Nessun avviso'
        return self.is_expiring_by_state() or self.is_expiring_by_urgency() or self.is_expiring_by_citation_date()

class EsecuzioneTerminiConCitazione(EsecuzioneConCitazione):
    def __init__(self, data_obj) -> None:
        self.dal_giorno = self.date_addition(self.date_parser(data_obj.get('Dal_giorno').get('value')), 1) if data_obj.get('Dal_giorno') else datetime.date.today()
        super().__init__(data_obj)
    
    def is_expiring_by_state(self) -> bool:
        return self.stato_desiderato and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_state) <= self.date_to_which_to_compare

    def is_expiring_by_urgency(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.modalita in ['OGGI', 'URGENTE'] and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_urgency) <= self.date_to_which_to_compare

class ImmissioneInPossesso(Esecuzione):
    def __init__(self, data_obj) -> None:
        self.data_esecuz = self.date_addition(self.date_parser(data_obj.get(
            'Data_esecuz').get('value')), 1) if data_obj.get('Data_esecuz') else datetime.date.today()
        super().__init__(data_obj)
        self.delta_num_of_days_for_esecuz = 3

    def is_expiring_by_execution_date(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.date_to_which_to_compare >= self.date_addition(self.data_esecuz, self.delta_num_of_days_for_esecuz)

    def is_expiring(self, date_to_which_to_compare: datetime.date) -> bool:
        self.date_to_which_to_compare = date_to_which_to_compare
        self.motivo_scadenza = self.motivo_scadenza_deposito if self.is_expiring_by_state() else self.motivo_scadenza_urgente_o_oggi if self.is_expiring_by_urgency() else self.motivo_scandeza_esecuzione if self.is_expiring_by_execution_date() else 'Nessun avviso'
        return self.is_expiring_by_state() or self.is_expiring_by_urgency() or self.is_expiring_by_execution_date()
class AttoDiAvviso(ImmissioneInPossesso):
    def __init__(self, data_obj) -> None:
        super().__init__(data_obj)
        self.delta_num_of_days_for_esecuz = 7

    def is_expiring_by_execution_date(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.date_to_which_to_compare >= self.date_subtraction(self.data_esecuz, self.delta_num_of_days_for_esecuz)

class Sequestro(ImmissioneInPossesso):
    '''Stesso comportamento di immissione in possesso'''
class SequestroTermini(ImmissioneInPossesso):
    def __init__(self, data_obj):
        self.dal_giorno = self.date_addition(self.date_parser(data_obj.get('Dal_giorno').get('value')), 1) if data_obj.get('Dal_giorno') else datetime.date.today()
        super().__init__(data_obj)
        self.stato_desiderato = "In itinere"
    
    def is_expiring_by_state(self) -> bool:
        return self.stato_desiderato and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_state) <= self.date_to_which_to_compare

    def is_expiring_by_urgency(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.modalita in ['OGGI', 'URGENTE'] and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_urgency) <= self.date_to_which_to_compare

class AttoDiAvvisoFissazione(Esecuzione):
    '''Stesso comportamento di sequestro termini: in itinere, dal giorno (anziché richiesta_del) ma non data esecuzione'''
    def __init__(self, data_obj):
        self.dal_giorno = self.date_addition(self.date_parser(data_obj.get('Dal_giorno').get('value')), 1) if data_obj.get('Dal_giorno') else datetime.date.today()
        super().__init__(data_obj)
        self.stato_desiderato = "In itinere"

    def is_expiring_by_state(self) -> bool:
        return self.stato_desiderato and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_state) <= self.date_to_which_to_compare

    def is_expiring_by_urgency(self) -> bool:
        return self.stato_desiderato and self.allarme == 'Avvisami' and self.modalita in ['OGGI', 'URGENTE'] and self.date_addition(self.dal_giorno, self.delta_num_of_days_for_urgency) <= self.date_to_which_to_compare

    def is_expiring(self, date_to_which_to_compare: datetime.date) -> bool:
        self.date_to_which_to_compare = date_to_which_to_compare
        self.motivo_scadenza = self.motivo_scadenza_deposito if self.is_expiring_by_state() else self.motivo_scadenza_urgente_o_oggi if self.is_expiring_by_urgency() else 'Nessun avviso'
        return self.is_expiring_by_state() or self.is_expiring_by_urgency()
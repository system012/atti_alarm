import datetime
import sys
from typing import List, Dict
from domain import atto_factory, Notificabile, Atto
from infrastructure import FetchClient
from infrastructure import write, read
from utils.constants import novadata_url
from presentation import telegram_based_reporting
from infrastructure import fields_renaming_mapper


def get_notifiable(atti_in_scadenza: List[Atto], atti_notificati: Dict, alarm_type) -> Dict:
    '''Checks whether expiring atti are notifiable and returns dict with notifiable atti as instances of class Notificabile'''

    atti_da_avvisare = {}
    nuovi_atti = [Notificabile.from_atto(nuovo_atto) for nuovo_atto in atti_in_scadenza if not atti_notificati.get(
        nuovo_atto.id_pex)]  # lista nuovi atti encapsulati in Notificabile
    vecchi_atti_avvisati = [Notificabile(atti_notificati.get(vecchio_atto.id_pex)) for vecchio_atto in atti_in_scadenza if atti_notificati.get(
        vecchio_atto.id_pex)]  # lista vecchi atti (già avvisati) che soddisfano ancora i requisiti delle rispettive classi (scadenza atto). Ora vengono encapsulati in Notificabile

    for atto in nuovi_atti:
        atto.set_data_avviso(datetime.date.today())
        if alarm_type == 'daily':
            atto.increase_numero_avvisi(1)
        atti_da_avvisare.update(atto.to_dict())

    for atto in vecchi_atti_avvisati:
        print(f"Atto {atto.id_pex}")
        if atto.is_notifiable(len(atti_da_avvisare)):
            atto.set_data_avviso(datetime.date.today())
            if alarm_type == 'daily':
                atto.increase_numero_avvisi(1)
            atti_da_avvisare.update(atto.to_dict())

    return atti_da_avvisare    

def main(alarm_type='weekly') -> None:
    '''Main function putting everything together'''

    client = FetchClient()

    client.fetch_data(novadata_url)

    entries = fields_renaming_mapper(client.entries)

    atti_in_scadenza = []
    dates_to_compare_to = {"weekly": datetime.date.today() + datetime.timedelta(days=7), "daily": datetime.date.today()}

    for data in entries:
        atto = atto_factory(data)
        if not atto:
            continue
        if atto.is_expiring(dates_to_compare_to[alarm_type]):
            atti_in_scadenza.append(atto)

    atti_notificati_salvati = read()

    atti_da_avvisare = get_notifiable(atti_in_scadenza, atti_notificati_salvati, alarm_type)

    atti_da_salvare_su_json = {**atti_notificati_salvati, **atti_da_avvisare}

    if atti_da_salvare_su_json:
        write(atti_da_salvare_su_json)

    if atti_da_avvisare:
      telegram_based_reporting(atti_da_avvisare, alarm_type)


if __name__ == "__main__":
    alarm_type_arg = sys.argv[1] # weekly oppure daily
    main(alarm_type_arg)

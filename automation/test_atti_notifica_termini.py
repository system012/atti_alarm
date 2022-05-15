from domain import *

def test_notifica_termini_stato_desiderato_in_itinere():
    entry = {'ID_PEX': {'id': 1, 'value': 2204100}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-18T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Non avvisarmi'}, 'Attività': {'id': 5, 'value': 'Notifica Termini Im'}, 'Atto': {'id': 6, 'value': 'Omologa'}, 'Modalità': {'id': 11, 'value': 'Normale'}, 'Tipologia': {'id': 14, 'value': '- Esente'}, 'Stato': {'id': 18, 'value': 'In itinere'}, 'Dal_giorno': {'id': 99, 'value': '2022-04-20T22:00:00.000Z'}}
    notifica = NotificaTerminiImerese(entry) # stato in itinere
    assert notifica.stato_desiderato == True

def test_notifica_termini_stato_desiderato_in_consegna():
    entry = {'ID_PEX': {'id': 1, 'value': 2204100}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-18T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Non avvisarmi'}, 'Attività': {'id': 5, 'value': 'Notifica Termini Im'}, 'Atto': {'id': 6, 'value': 'Omologa'}, 'Modalità': {'id': 11, 'value': 'Normale'}, 'Tipologia': {'id': 14, 'value': '- Esente'}, 'Stato': {'id': 18, 'value': 'In consegna'}, 'Dal_giorno': {'id': 99, 'value': '2022-04-20T22:00:00.000Z'}}
    notifica = NotificaTerminiImerese(entry) # stato in itinere
    assert notifica.stato_desiderato == False

def test_notifica_termini_is_expiring_by_state():
    entry = {'ID_PEX': {'id': 1, 'value': 2204100}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-18T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Non avvisarmi'}, 'Attività': {'id': 5, 'value': 'Notifica Termini Im'}, 'Atto': {'id': 6, 'value': 'Omologa'}, 'Modalità': {'id': 11, 'value': 'Normale'}, 'Tipologia': {'id': 14, 'value': '- Esente'}, 'Stato': {'id': 18, 'value': 'In itinere'}, 'Dal_giorno': {'id': 99, 'value': '2022-03-20T22:00:00.000Z'}}
    notifica = NotificaTerminiImerese(entry)
    assert notifica.is_expiring(datetime.date.today()) == True

def test_notifica_termini_is_expiring_by_urgency():
    entry = {'ID_PEX': {'id': 1, 'value': 2204100}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-18T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Avvisami'}, 'Attività': {'id': 5, 'value': 'Notifica Termini Im'}, 'Atto': {'id': 6, 'value': 'Omologa'}, 'Modalità': {'id': 11, 'value': 'URGENTE'}, 'Tipologia': {'id': 14, 'value': '- Esente'}, 'Stato': {'id': 18, 'value': 'In itinere'}, 'Dal_giorno': {'id': 99, 'value': '2022-04-12T22:00:00.000Z'}}
    notifica = NotificaTerminiImerese(entry)
    assert notifica.is_expiring(datetime.date.today()) == True

def test_notifica_termini_is_expiring_by_urgency_with_non_avvisarmi_filter():
    entry = {'ID_PEX': {'id': 1, 'value': 2204100}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-18T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Non avvisarmi'}, 'Attività': {'id': 5, 'value': 'Notifica Termini Im'}, 'Atto': {'id': 6, 'value': 'Omologa'}, 'Modalità': {'id': 11, 'value': 'URGENTE'}, 'Tipologia': {'id': 14, 'value': '- Esente'}, 'Stato': {'id': 18, 'value': 'In itinere'}, 'Dal_giorno': {'id': 99, 'value': '2022-04-12T22:00:00.000Z'}}
    notifica = NotificaTerminiImerese(entry)
    assert notifica.is_expiring(datetime.date.today()) == False
from domain import *

def test_notifica_SR_esente_expiry(): # stato in gestione
    entry = {'ID_PEX': {'id': 1, 'value': 2204033}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-05T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Avvisami'}, 'Attività': {'id': 5, 'value': 'Notifica SR'}, 'Atto': {'id': 6, 'value': 'Precetto'}, 'Modalità': {'id': 11, 'value': 'Normale'}, 'Tipologia': {'id': 14, 'value': '- Esente'}, 'Stato': {'id': 18, 'value': 'In gestione'}, 'Richiesta_del': {'id': 20, 'value': '2022-03-06T22:00:00.000Z'}}
    notifica = Notifica_SR(entry)
    assert notifica.is_expiring(datetime.date.today()) == True

def test_notifica_SR_pagamento_expiry_by_state(): # stato in corso di notifica
    entry = {'ID_PEX': {'id': 1, 'value': 2204033}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-05T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Avvisami'}, 'Attività': {'id': 5, 'value': 'Notifica SR'}, 'Atto': {'id': 6, 'value': 'Precetto'}, 'Modalità': {'id': 11, 'value': 'Normale'}, 'Tipologia': {'id': 14, 'value': '- Pagamento'}, 'Stato': {'id': 18, 'value': 'In corso di notifica'}, 'Richiesta_del': {'id': 20, 'value': '2022-03-06T22:00:00.000Z'}}
    notifica = Notifica_SR(entry)
    assert notifica.is_expiring(datetime.date.today()) == True

def test_notifica_SR_pagamento_expiry_by_urgency(): # stato in corso di notifica
    entry = {'ID_PEX': {'id': 1, 'value': 2204033}, 'Cod_PEX_del': {'id': 2, 'value': '2022-04-05T22:00:00.000Z'}, 'Allarme': {'id': 138, 'value': 'Avvisami'}, 'Attività': {'id': 5, 'value': 'Notifica SR'}, 'Atto': {'id': 6, 'value': 'Precetto'}, 'Modalità': {'id': 11, 'value': 'URGENTE'}, 'Tipologia': {'id': 14, 'value': '- Pagamento'}, 'Stato': {'id': 18, 'value': 'In corso di notifica'}, 'Richiesta_del': {'id': 20, 'value': '2022-04-10T22:00:00.000Z'}}
    notifica = Notifica_SR(entry)
    assert notifica.motivo_scadenza == "Urgente/Oggi"
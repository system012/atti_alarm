from typing import Dict
from domain import (Atto, AttoDiAvvisoFissazione, EsecuzioneTerminiConCitazione, 
                    Notifica, Notifica_SR, NotificaConCitazione,  NotificaTerminiImerese, Esecuzione, 
                    EsecuzioneConCitazione, AttoDiAvviso, ImmissioneInPossesso, Sequestro, SequestroTermini)

def atto_factory(atto: Dict) -> Atto:
    attivita = atto.get('Attività').get('value')

    if attivita.startswith('Notifica'):
        return notifica_factory(atto)

    if attivita.startswith('Esecuzione') or attivita.startswith('Fiss data'):
        return esecuzione_factory(atto)

    return None

def notifica_factory(data: Dict) -> Notifica:
    attivita = data.get('Attività').get('value')
    atto = data.get('Atto').get('value')

    match attivita:
        case 'Notifica SR':
            return Notifica_SR(data)

    match [attivita, atto.startswith('Citazione')]:
        case ['Notifica', True]:
            return NotificaConCitazione(data)

    match attivita:
        case 'Notifica Termini Im':
            return NotificaTerminiImerese(data)

    match attivita.startswith('Notifica'):
        case True:
            return Notifica(data)


def esecuzione_factory(data: Dict) -> Esecuzione:
    attivita = data.get('Attività').get('value')
    atto = data.get('Atto').get('value')

    match [attivita, atto]:
        case ['Esecuzione', 'Sequestro']:
            return Sequestro(data)

    match [attivita, atto]:
        case ['Esecuzione Termini Im', 'Sequestro']:
            return SequestroTermini(data)

    match [attivita, atto]:
        case ['Esecuzione', 'Pignoramento PT']:
            return EsecuzioneConCitazione(data)

    match [attivita, atto]:
        case ['Esecuzione Termini Im', 'Pignoramento PT']:
            return EsecuzioneTerminiConCitazione(data)

    match [attivita, atto]:
        case ['Esecuzione', 'Imm in possesso']:
            return ImmissioneInPossesso(data)

    match [attivita, atto]:
        case ['Esecuzione', 'Atto di Avviso']:
            return AttoDiAvviso(data)

    match [attivita.startswith('Fiss data'), atto]:
        case [True, 'Atto di Avviso']:
            print(data.get('ID_PEX').get('value'))
            return AttoDiAvvisoFissazione(data)

    match attivita:
        case 'Esecuzione':
            return Esecuzione(data)
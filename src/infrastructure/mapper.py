from typing import Dict, List

def map_memento_fields_to_named_fields(entry: Dict) -> Dict:
    '''Make memento fields more readable by assigning them a name instead of an ID. E.g. ID_PEX, Attività etc.'''
    fields_obj = {}

    for field in entry.get('fields'):
        match field['id']:
            case 1:
                fields_obj.update({'ID_PEX': field})

            case 5:
                fields_obj.update({'Attività': field})

            case 6:
                fields_obj.update({'Atto': field})

            case 11:
                fields_obj.update({'Modalità': field})

            case 14:
                fields_obj.update({'Tipologia': field})

            case 16:
                fields_obj.update({'Data_esecuz': field})

            case 17:
                fields_obj.update({'Data_citazione': field})

            case 18:
                fields_obj.update({'Stato': field})

            case 20:
                fields_obj.update({'Richiesta_del': field})

            case 99:
                # l'equivalente di richiesta_del di termini imerese
                fields_obj.update({'Dal_giorno': field})

            case 138:
                fields_obj.update({'Allarme': field})

            case 153:
                fields_obj.update({'Cod_PEX_del': field})

    return fields_obj

def fields_renaming_mapper(entries: List[Dict]) -> List[Dict]:
    '''Transforms list of many unnamed dicts into list of named dicts for each memento field'''
    new_list = []

    for entry in entries:
        new_obj = map_memento_fields_to_named_fields(entry)
        new_list.append(new_obj)

    return new_list

def map_named_fields_to_memento(atti: Dict) -> Dict:
    '''Remaps fields from notifiable to a dict with the same structure of memento'''

    entries = []

    for atto in atti.values():
        entries.append( 
            {
                "fields": [
                {
                    "id": 2,
                    "value": atto.get('id_pex')
                },
                {
                    "id": 8,
                    "value": atto.get("attivita")
                },
                {
                    "id": 3,
                    "value": atto.get('atto')
                },
                {
                    "id": 4,
                    "value": atto.get('motivo_scadenza')
                },
                {
                    "id": 5,
                    "value": atto.get('numero_avvisi')
                },
                {
                    "id": 7,
                    "value": atto.get('data_allarme')
                },
                ]
            })
    
    return entries

from jinja2 import Environment, FileSystemLoader
import datetime
import time
import json
from typing import Dict
from utils.utility import get_actual_path
from infrastructure import FetchClient
from utils.utility import filter_atti_by_attivita, reorder_atti_by_date
from presentation import send_document
from infrastructure import map_named_fields_to_memento

def telegram_based_reporting(atti: Dict, alarm_type) -> None:
    notifiche = filter_atti_by_attivita(atti, "Notifica") # filtra gli atti da avvisare per attività che iniziano con "Notifica"
    esecuzioni = filter_atti_by_attivita(atti, "Esecuzione") # filtra gli atti da avvisare per attività che iniziano con "Esecuzione"

    print(f"Notifiche: {notifiche}")
    print(f"Esecuzioni: {esecuzioni}")

    report_file_name = {'weekly': 'report_settimanale.html', 'daily': 'report.html'}

    if notifiche or esecuzioni:
        sorted_notifiche = reorder_atti_by_date(notifiche) # ordina le notifiche per data_scadenza
        sorted_esecuzioni = reorder_atti_by_date(esecuzioni) # ordina le esecuzioni per data_scadenza
        generate_html_report(sorted_notifiche, sorted_esecuzioni, report_file_name, report_type=alarm_type)
        send_document(get_actual_path(*['reports', report_file_name[alarm_type]]))

def memento_based_reporting(atti: Dict, url: str) -> None:
    entries = map_named_fields_to_memento(atti)
    generate_memento_report(entries, url)

def generate_memento_report(entries: dict, url: str) -> None:
    for entry in entries:
        client = FetchClient()
        client.post_data(url, json.dumps(entry))
        time.sleep(1)

def generate_html_report(notifiche_data: dict, esecuzioni_data: dict, report_file_name, report_type='weekly') -> None:
    page_title = {'weekly': f'Report settimanale {datetime.date.today().strftime("%d/%m/%Y")}', 'daily': f'Report giornaliero {datetime.date.today().strftime("%d/%m/%Y")}'}

    file_loader = FileSystemLoader(searchpath=get_actual_path('templates'))
    env = Environment(loader=file_loader, autoescape=True)

    template = env.get_template(report_file_name[report_type])

    output = template.render(notifiche_data=notifiche_data, esecuzioni_data=esecuzioni_data, page_title=page_title[report_type], notifiche_length=len(notifiche_data), esecuzioni_length=len(esecuzioni_data))

    write_to_html(output, get_actual_path(*['reports', report_file_name[report_type]]))

    print(f'Creato {report_file_name[report_type]}!')

def generate_telegram_report(notifiche, esecuzioni):
    notifiche_msg_list = []
    esecuzioni_msg_list = []

    if notifiche:
        notifiche_msg_list = [f"{index+1}) {element.get('id_pex')}" + " - " + f"{element.get('atto')}" + " - " + f"Motivo: {element.get('motivo_avviso')}" + " - " + f"Avvisi: {element.get('numero_avvisi')}" 
                                for index, element in enumerate(notifiche.values())]
    
    if esecuzioni:
        esecuzioni_msg_list = [f"{index+1}) {element.get('id_pex')}" + " - " + f"{element.get('atto')}" + " - " + f"Motivo: {element.get('motivo_avviso')}" + " - " + f"Avvisi: {element.get('numero_avvisi')}" 
                                for index, element in enumerate(esecuzioni.values())]
    
    notifiche_msg = '''NOTIFICHE:
    {0}'''.format("\n".join(notifiche_msg_list)) if notifiche_msg_list else ''
    
    esecuzioni_msg = '''ESECUZIONI:
    {0}'''.format("\n".join(esecuzioni_msg_list)) if esecuzioni_msg_list else ''

    return '\n\n'.join([notifiche_msg, esecuzioni_msg])

def write_to_html(html_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
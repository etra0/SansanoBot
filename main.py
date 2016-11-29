import re
import requests
from functions import *
from telegram_api import *
from secret_token import token
last = 0
while True:
    if get_updates():
        last_user = get_updates()["result"][-1]
    else:
        continue
    actual_id = last_user["update_id"]
    mensaje = last_user["message"]['text']
    if actual_id != last:
        try:
            print("%s %s: %s" % (time.strftime("%d/%m/%Y - %H:%M:%S"), last_user['message']['from']['username'], mensaje))
        except:
            print("%s %s: %s" % (time.strftime("%d/%m/%Y - %H:%M:%S"), last_user['message']['from']['first_name'], mensaje))

        last = actual_id
        last_id = last_user['message']['from']['id']

        minuta_match = re.match(minuta_regex, mensaje)
        minuta_match = minuta_match.groups() if minuta_match != None else False
        if minuta_match:
            print(minuta_match)
            send_message(minuta(minuta_regex_matches[minuta_match[1]], minuta_match[1], True if minuta_match[2] != None else False) if minuta_match[1] in minuta_regex_matches else "No existe ese menú", last_id)

        elif "/start" in mensaje or "/help" in mensaje:
            WELCOME_MESSAGE + ("\nCreado por @EtraStyle" if "/start" in mensaje else "")
            send_message(mensaje, last_id)

        elif "/clima" in mensaje:
            send_message("Actualmente, se encuentra en desarrollo.", last_id)
        else:
            send_message("Lo siento, no entiendo lo que quieres decir\n", last_id)

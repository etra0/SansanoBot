import re
from functions import *
from telegram_api import *
from secret_token import owner_id
import sys

WELCOME_MESSAGE = """                   <b>¡Bienvenido!</b>
Actualmente, el bot USM-Bot tiene los siguientes comandos:
- <i>minuta:</i> te otorga la minuta del día, ya sea normal, vegetariano ó dieta. Además, puedes solicitar solo la del día.
    <i>minuta [vegetariano|normal|dieta] [hoy]</i>
<i>Ejemplo</i>
<b>/minuta vegetariano hoy</b>
- <i>clima:</i> te otorga el clima en la universidad. (EN DESARROLLO)
    <i>[/]clima [hoy]</i>

Lo que está en [corchetes] es opcional.
"""
commands = [r"[/]?([mM]inuta)(?: (?P<type_lunch>vegetariano|dieta|normal))?(?: (?P<today>hoy))?",
            r"[/](start|help)",
            r"[/]?(clima)(?: (?P<today>hoy))?"
            ]

commands = init_regex(commands)

def main():
    last_message_id = 0
    while True:
        try:
            updates = get_updates()
        except Exception as err:
            print("Probablemente hayan problemas de conexion: %s" % err)
            continue

        if updates and len(updates) > 1:
            last_user = updates["result"][-1]
        else:
            continue
        actual_message_id = last_user["update_id"]
        message = last_user["message"]['text']
        if actual_message_id != last_message_id:
            if 'username' in last_user['message']['from']:
                print("%s %s: %s" % (time.strftime("%d/%m/%Y - %H:%M:%S"), last_user['message']['from']['username'], message))
            else:
                print("%s %s: %s" % (time.strftime("%d/%m/%Y - %H:%M:%S"), last_user['message']['from']['first_name'], message))

            last_message_id = actual_message_id
            last_user_id = last_user['message']['from']['id']

            for command in commands:
                command_match = command.match(message)
                if command_match:
                    command_name = command_match.group(1).lower()
                    command_dict = command_match.groupdict()
                    break

            if not command_match:
                send_message("No entiendo lo que quieres decir.", last_user_id)
                continue

            if command_name == "minuta":
                new_message = minuta(**command_dict)
                send_message(new_message, last_user_id)

            elif command_name == "clima":
                send_message(get_weather(**command_dict), last_user_id)

            elif command_name in "starthelp":
                new_message = WELCOME_MESSAGE + ("\nCreado por @EtraStyle" if "/start" in message else "")
                send_message(new_message, last_user_id)

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        send_message("Se ha cerrado SansanoBot, motivo:\n%s" % err, owner_id)
        sys.exit()

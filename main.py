import re
import sys
import logging
from lib.constants import *
from lib.functions import *
from lib.telegram_api import *
from lib.secret_token import owner_id
from lib.weather import Clima, interface

class FilterOne:
    def __init__(self, level):
        self.level = level

    def filter(self, verified):
        return self.level == verified.levelno

commands = [r"[/]?([mM]inuta)"
            + "(?: (?P<type_lunch>vegetariano|dieta|normal))?"
            + "(?: (?P<week>semana))?",
            r"[/](start|help)",
            r"[/]?(clima)(?: (?P<today>hoy))?"
            ]

# Para agregar una nueva funcion, agregar a funciones_dict, esta debe
# retornar un string.
# Tambien se debe agregar su expresion regular, y la funcion debe
# manejar todas las variables.
functions_dict = {
    "minuta": minuta,
    "clima": interface
}

commands = init_regex(commands)

def main():
    # inicializar logging
    logging.basicConfig(filename='logs/all.log', level=logging.DEBUG)

    logging_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt=TIME_FORMAT)

    # main log
    logger = logging.getLogger('class_logger')
    logger.setLevel(logging.DEBUG)


    all_log = logging.FileHandler('logs/sansanobot.log')
    all_log.setLevel(logging.DEBUG)
    all_log.setFormatter(logging_formatter)
    logger.addHandler(all_log)

    # historial log
    historial_formatter = logging.Formatter(
            "%(asctime)s - %(message)s",
            datefmt=TIME_FORMAT)

    historial_log = logging.FileHandler('logs/historial.log')
    historial_log.setLevel(logging.INFO)

    #in this case, we need the info log, so I created a class called FilterOne
    historial_log.addFilter(FilterOne(logging.INFO))
    historial_log.setFormatter(historial_formatter)
    logger.addHandler(historial_log)

    # stream log
    stream_log = logging.StreamHandler()
    stream_log.setLevel(logging.INFO)
    stream_log.addFilter(FilterOne(logging.INFO))
    stream_log.setFormatter(historial_formatter)
    logger.addHandler(stream_log)


    last_message_id = 0
    offset = -9
    while offset == -9:
        updates = get_updates()

        if updates and len(updates["result"]) > 1:
            offset = updates["result"][-1]["update_id"]
            break
        else:
            continue

    while True:
        # Usualmente falla porque el laboratorio se queda sin internet
        # en ciertos momentos del dia.
        try:
            updates = get_updates(offset)
        except Exception as err:
            logger.warning(err)
            continue

        # A veces retornaba una lista de resultados vacia, por ende,
        # es necesario que al menos obtenga una solicitud
        if updates and len(updates["result"]) > 1:
            last_user = updates["result"][-1]
        else:
            continue

        actual_message_id = last_user["update_id"]

        # Podian existir mensajes sin textos, por ejemplo:
        # los stickers.
        if 'text' in last_user['message']:
            message = last_user["message"]['text']
        else:
            continue

        if actual_message_id != last_message_id:
            if 'username' in last_user['message']['from']:

                to_print = "%s: %s" % (
                    last_user['message']['from']['username'], message)

                logger.info(to_print)
            else:

                to_print = "%s: %s" % (
                    last_user['message']['from']['first_name'], message)

                logger.info(to_print)

            last_message_id = actual_message_id
            last_user_id = last_user['message']['from']['id']

            for command in commands:
                command_match = command.match(message)
                if command_match:
                    command_name = command_match.group(1).lower()
                    command_dict = command_match.groupdict()
                    break

            if not command_match:
                send_message("No entiendo lo que quieres decir.",
                        last_user_id)
                continue

            if command_name in functions_dict:
                new_message = functions_dict[command_name](**command_dict)
                send_message(new_message, last_user_id)

            elif command_name in "starthelp":
                new_message = WELCOME_MESSAGE \
                     + ("\nCreado por @EtraStyle" \
                             if "/start" in message else "")
                send_message(new_message, last_user_id)

            offset += 1

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        send_message("Se ha cerrado SansanoBot, motivo:\n%s" % err, owner_id)
        sys.exit()

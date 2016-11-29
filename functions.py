import re
import time
import requests

WELCOME_MESSAGE = """                   <b>¡Bienvenido!</b>
Actualmente, el bot USM-Bot tiene los siguientes comandos:
- <i>minuta:</i> te otorga la minuta del día, ya sea normal, vegetariano ó dieta. Además, puedes solicitar solo la del día.
<i>Ejemplo</i>
<b>/minuta vegetariano hoy</b>
- <i>clima:</i> te otorga el clima del día en la universidad. (EN DESARROLLO)

"""

minuta_regex = r"([/]?[mM]inuta)(?P<type> vegetariano| dieta| normal)?(?P<today> hoy)?"
minuta_regex = re.compile(minuta_regex)
minuta_regex_matches = {
    None: 0,
    "normal": 0,
    "dieta": 1,
    "vegetariano": 2
}

def minuta(determinante, nombre, hoy):
    regex = re.compile(r"<table>(.*?)</table>", re.DOTALL)
    try:
        minuta = requests.get('http://www.usm.cl/comunidad/servicio-de-alimentacion/')
    except:
        send_message("Time out")
        if minuta.status_code != 200:
            send_message("No se pudo conectar!")
    minuta_text = minuta.text.strip()
    minuta_text = regex.search(minuta_text).groups()[0].strip().split("\n")

    # Luego es necesario remover todos los elementos vacios, y ademas aplicar strip a cada string.
    while '' in minuta_text:
        minuta_text.remove('')
    minuta_text = list(map(lambda string: string.strip(), minuta_text))
    minuta_text = "\n".join(minuta_text)

    regex = re.compile(r"<td>(.+?)</td>", re.DOTALL)
    minuta_text = regex.findall(minuta_text)

    # Informacion irrelevante en minuta
    minuta_text.remove("<p><strong>&nbsp;</strong></p>")
    minuta_text.remove("<p><strong>Almuerzos</strong></p>")

    # Se quitan las ultimas etiquetas innecesarias
    minuta_text = list(map(lambda string: re.sub(r"</?(?:p|strong)>", "", string), minuta_text))

    if not nombre:
        nombre = "normal"

    text = "<b>Minuta %s\n\n</b>" % nombre.title()

    weekday = int(time.strftime("%w"))
    if not hoy or weekday > 5:
        for i in range(0, 5):
            text += "<b>%s</b>:\n" % minuta_text[i].strip() + minuta_text[i + 5 * (determinante + 1) + determinante].strip() + "\n\n"
    else:
        text += "<b>Hoy %s</b>:\n" % minuta_text[weekday - 1].strip() + minuta_text[weekday - 1 + 5*(determinante + 1) + determinante].strip() + "\n"

    return text

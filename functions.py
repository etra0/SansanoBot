import re
import urllib, json
import requests
import time
from urllib.parse import quote


def init_regex(regex_list):
    regex_list = list(map(lambda regex: re.compile(regex), regex_list))
    return regex_list

def minuta(type_lunch, week):
    type_lunch_number = {
        None: 0,
        "normal": 0,
        "dieta": 1,
        "vegetariano": 2
    }
    factor = type_lunch_number[type_lunch]


    try:
        minuta = requests.get('http://www.usm.cl/comunidad/servicio-de-alimentacion/')
    except requests.exceptions.ConnectTimeout as err:
        return "No se ha podido conectar con usm.cl"

    if minuta.status_code != 200:
        send_message("No se pudo conectar!")

    regex = re.compile(r"<table>(.*?)</table>", re.DOTALL)
    minuta_text = minuta.text.strip()
    minuta_text = regex.search(minuta_text).group(1)

    regex = re.compile(r"<td>(.+?)</td>", re.DOTALL)
    minuta_text = regex.findall(minuta_text)

    # Informacion irrelevante en minuta
    minuta_text.remove("<p><strong>&nbsp;</strong></p>")
    minuta_text.remove("<p><strong>Almuerzos</strong></p>")

    # Se quitan las ultimas etiquetas innecesarias
    minuta_text = list(map(lambda string: re.sub(r"</?(?:p|strong)>", "", string), minuta_text))

    if not type_lunch:
        type_lunch = "normal"

    # Fixes de espacios cuestionables de los malos programadores
    # de la USM.
    regex_spaces = re.compile(r"[ ]+", re.DOTALL)
    for i in range(len(minuta_text)):
        minuta_text[i] = re.sub(regex_spaces, " ", minuta_text[i])

    text = "<b>Minuta %s\n\n</b>" % type_lunch.title()

    weekday = int(time.strftime("%w"))
    if week or weekday > 5:
        for i in range(0, 5):
            text += "<b>%s</b>:\n" % minuta_text[i].strip() + minuta_text[i + 5 * (factor + 1) + factor].strip() + "\n\n"
    else:
        text += "<b>Hoy %s</b>:\n" % minuta_text[weekday - 1].strip() + minuta_text[weekday - 1 + 5*(factor + 1) + factor].strip() + "\n"

    return text

def to_celsius(f):
    return (f - 32) / 1.8

def load_weather_code():
    weather_code_dict = dict()
    with open('weather_code') as txt:
        for line in txt:
            line = line.strip().split(";")
            weather_code_dict[line[0]] = line[1]
    return weather_code_dict

weather_code_dict = load_weather_code()

def get_weather(today):
    yahoo_time_format = "%y-%m-%dT%h:%M:%SZ"
    translate_days = {
        'Mon': "Lunes",
        'Tue': "Martes",
        "Wed": "Miércoles",
        "Thu": "Jueves",
        "Fri": "Viernes",
        "Sat": "Sábado",
        "Sun": "Domingo"
    }

    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    woeid_USM = "349526"
    yql_query = "select * from weather.forecast where woeid={id_usm}".format(id_usm=woeid_USM)
    yql_url = baseurl + 'q=' + quote(yql_query) + "&format=json"
    try:
        result = urllib.request.urlopen(yql_url)
        data = json.loads(result.read().decode('utf-8'))
        weather = data['query']['results']['channel']['item']['forecast']
    except:
        return "No se pudo obtener el clima 😢"

    # We need to convert all the days to Celsius.
    for day in range(len(weather)):
        weather[day]['high'] = to_celsius(int(weather[day]['high']))
        weather[day]['low'] = to_celsius(int(weather[day]['low']))

    if today:
        text = "<b>Pronóstico hoy (%s):</b>\n" % weather[0]['date']
        text += weather_code_dict[weather[0]['code']] + "\n"
        text += "Máxima: %dºC 🌈\nMínima: %dºC 🌠" % (weather[0]['high'], weather[0]['low'])
    else:
        text = "<b>Pronóstico durante los siguientes %d días:</b>\n\n" % len(weather)
        for day in range(len(weather)):
            text += "<b>%s, %s:</b>\n" % (translate_days[weather[day]['day']], weather[day]['date'])
            text += weather_code_dict[weather[day]['code']] + "\n"
            text += "Máxima: %dºC 🌈\nMínima: %dºC 🌠\n\n" % (weather[day]['high'], weather[day]['low'])

    return text

if __name__ == "__main__":
    print(get_weather(True))

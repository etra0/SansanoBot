#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote
import urllib, json
import requests
import time
import re
from secret_token import token

minuta_regex = r"([/]?[mM]inuta) ?(vegetariano|dieta|normal|\w+)? ?(hoy)?"
minuta_regex = re.compile(minuta_regex)
minuta_regex_matches = {
    None: 0,
    "normal": 0,
    "dieta": 1,
    "vegetariano": 2
}

def getMe():
    url = "https://api.telegram.org/%s/getMe" % token
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

def getUpdates():
    url = "https://api.telegram.org/%s/getUpdates" % token
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

def sendMessage(text, user):
    url = "https://api.telegram.org/%s/sendMessage?chat_id=" % token + str(user) + "&parse_mode=HTML&text="
    url += quote(text)
    response = urllib.request.urlopen(url)
    try:
        data = json.loads(response.read())
        return data
    except:
        pass

def minuta(determinante, nombre, hoy):
    try:
        minuta = requests.get('http://www.usm.cl/comunidad/servicio-de-alimentacion/')
    except:
        sendMessage("Time out")
        if minuta.status_code != 200:
            sendMessage("No se pudo conectar!")
    minuta_text = minuta.text.strip().split('\n')
    leer = False
    info = []
    for linea in minuta_text:
        if "<table>" in linea:
            leer = True
            continue
        if "</table>" in linea:
            leer = False
            continue
        if leer and linea != '' and "col width=" not in linea and "&nbsp" not in linea:
            info.append(linea.strip().replace("<p>", "").replace("</p>", ""))

    info = "\n".join(info)
    info = info.strip().split("</td>")
    info.remove("\n</tr>\n<tr>\n<td><strong>Almuerzos</strong>")
    for i in range(len(info)):
        info[i] = info[i].replace("<td>","").replace("<strong>", "").replace("</strong>", "").replace("<tr>", "")

    if nombre == None:
        nombre = "normal"
    text = "<b>Minuta %s\n\n</b>" % nombre.title()
    weekday = int(time.strftime("%w"))
    if not hoy or weekday > 5:
        for i in range(0, 5):
            text += "<b>%s</b>:\n" % info[i].strip() + info[i + 5*(determinante + 1) + determinante].strip() + "\n\n"
    else:
        text += "<b>Hoy %s</b>:\n" % info[weekday - 1].strip() + info[weekday - 1 + 5*(determinante + 1) + determinante].strip() + "\n"


    return text


last = 0
while True:
    last_user = getUpdates()["result"][-1]
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
            sendMessage(minuta(minuta_regex_matches[minuta_match[1]], minuta_match[1], True if minuta_match[2] != None else False) if minuta_match[1] in minuta_regex_matches else "No existe ese menú", last_id)

        elif "/start" in mensaje or "/help" in mensaje:
            mensaje = """                   <b>¡Bienvenido!</b>
Actualmente, el bot USM-Bot tiene los siguientes comandos:
    - <i>minuta:</i> te otorga la minuta del día, ya sea normal, vegetariano ó dieta. Además, puedes solicitar solo la del día.
    <i>Ejemplo</i>
        <b>/minuta vegetariano hoy</b>
    - <i>clima:</i> te otorga el clima del día en la universidad. (EN DESARROLLO)

""" + ("\nCreado por @EtraStyle" if "/start" in mensaje else "")
            sendMessage(mensaje, last_id)

        elif "/clima" in mensaje:
            sendMessage("Actualmente, se encuentra en desarrollo.", last_id)
        else:
            sendMessage("Lo siento, no entiendo lo que quieres decir\n", last_id)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote
import urllib, json
import requests
import time

def getMe():
    url = "https://api.telegram.org/bot282934143:AAFdnIgRuK50WJQO0sZxdqpaxrOxuNrZrTs/getMe"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

def getUpdates():
    url = "https://api.telegram.org/bot282934143:AAFdnIgRuK50WJQO0sZxdqpaxrOxuNrZrTs/getUpdates"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

def sendMessage(text, user):
    url = "https://api.telegram.org/bot282934143:AAFdnIgRuK50WJQO0sZxdqpaxrOxuNrZrTs/sendMessage?chat_id=" + str(user) + "&parse_mode=HTML&text="
    url += quote(text)
    response = urllib.request.urlopen(url)
    try:
        data = json.loads(response.read())
        return data
    except:
        pass

def minuta():
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

    text = ""
    for i in range(0, 5):
        text += "<b>%s</b>:\n" % info[i].strip() + info[i+5].strip() + "\n\n"

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
        if "minuta" in mensaje:
            sendMessage(minuta(), last_id)
        elif "/start" in mensaje or "/help" in mensaje:
            mensaje = """                   <b>¡Bienvenido!</b>
Actualmente, el bot USM-Bot tiene los siguientes comandos:
    - <i>minuta:</i> te otorga la minuta del día.
    - <i>clima:</i> te otorga el clima del día en la universidad. (EN DESARROLLO)

<b>Por integrar</b>: minuta vegana, y dieta.
""" + ("\nCreado por @EtraStyle" if "/start" in mensaje else "")
            sendMessage(mensaje, last_id)
        else:
            sendMessage("Lo siento, no entiendo lo que quieres decir\n", last_id)

import re
from html import unescape
import requests as r

#TODO: generate a function to verify if the file is changed or not,
# so we don't need to create a new instance of Clima every time that
# a user call this one.
class Clima(object):
    data_dict = {}
    def __init__(self, text):
        self.data_dict = self.parse_meteochile(text)
        self.add_emojis()

    def add_emojis(self):
        emojis_dict = {
            r"[Nn]ub": "☁️",
            r"[Cc]ubier": "⛅️",
            r"[Cc]hubas|[Ll](?:uvia|ovizn)|[Pp]recip": "☔️",
            r"[Dd]esp|[Ss]ol": "☀️"
        }

        for i in range(len(self.data_dict['texto'])):
            for j in range(len(self.data_dict['texto'][i])):
                # we add the emojis accum just in case the regex can't manage
                # some weird chars.
                stack_emojis = ''
                for regex in emojis_dict:
                    match = re.findall(regex, self.data_dict['texto'][i][j])
                    if match:
                        # add space one time
                        if ' ' not in stack_emojis:
                            stack_emojis += ' '
                        stack_emojis += emojis_dict[regex]
                self.data_dict['texto'][i][j] += stack_emojis

    def parse_meteochile(self, text):
        dict_regex = re.compile(r"([\w_]+?) ?:")

        # Remove first 3 lines
        text = "\n".join(text.split("\n")[3:])

        #just parsing
        text = text.replace("Pronostico.push(", "")
        text = text.replace("});", "}")
        text = dict_regex.sub("'\\1' :", text, count=10000)

        # with this we find just the info of valparaiso.
        find_valpo = re.compile(r".*?('indice' : \"valpo\".*?)}", re.DOTALL)
        text = find_valpo.match(text)
        if not text:
            return False

        text = "{" + text.group(1).strip() + "}"
        data_dict = eval(text)

        return data_dict

    def generate_string(self):
        JORNADAS = ['<b>Madrugada:</b> ', '<b>Mañana:</b> ', \
                    '<b>Tarde:</b> ', '<b>Noche:</b> ']
        local_dict = self.data_dict

        # la cantidad de fechas dependen de la temperatura.
        dates = local_dict['fecha'][:len(local_dict['temperatura'])]
        temperatures = list(map(lambda x: x.split("/"),
                    local_dict['temperatura']))
        all_text = []
        for i, day in enumerate(dates):
            min_C, max_C = temperatures[i]
            weather_text = local_dict['texto'][i]
            # We have to join the inverse of them, because sometimes
            # the first text of the weather is missing, meaning that
            # the weather of that 'time' is useless now.
            weather_text = list(
                    zip(JORNADAS[::-1], weather_text[::-1]))[::-1]

            for i, tup in enumerate(weather_text):
                j, w = tup
                if not w:
                    del weather_text[i]

            weather_text = list(map(lambda x: "".join(x), weather_text))
            data_to_print = {
                'day': day.title(),
                'weather': "\n".join(weather_text),
                'min': min_C,
                'max': max_C
            }
            all_text.append(("{day}:\n" \
                        + ("Mínima {min} ºC, " if min_C else "") \
                        + "Máxima {max} ºC.\n" \
                        + "{weather}").format(
                            **data_to_print))
        return all_text



    def __str__(self):
        return "\n\n".join(self.generate_string())

def interface(today):
    js_text = unescape(open('data.js').read())
    try:
        c = Clima(js_text)
    except:
        return "No se ha podido obtener el clima"
    if today:
        return c.generate_string()[0]

    return "\n\n".join(c.generate_string())

if __name__ == "__main__":
    js_text = unescape(open('data.js').read())
    c = Clima(js_text)
    print(c)

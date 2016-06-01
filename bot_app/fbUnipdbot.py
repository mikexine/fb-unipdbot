# -*- coding: utf-8 -*-

import requests
import ConfigParser
import os
import datetime
import json

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + "/settings.ini")
token = str(config.get('main', 'token'))

FB_URL = "https://graph.facebook.com/v2.6/me/messages?access_token=" + token

API_URL = "http://52.58.83.94/api/unipd/"


HEADERS = {"Content-Type": "application/json"}

TEXT_MESSAGE = {
    "recipient": {
        "id": "USER_ID"
    },
    "message": {
        "text": "hello, world!"
    }
}

IMAGE_MESSAGE = {
    "recipient": {
        "id": "USER_ID"
    },
    "message": {
        "attachment": {
            "type": "image",
            "payload": {
                "url": "IMAGE_URL"
            }
        }
    }
}


BUTTON_MESSAGE = {
    "recipient": {
        "id": "USER_ID"
    },
    "message": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "TEXT",
                "buttons": []
            }
        }
    }
}

BUTTON_POSTBACK = [{
    "type": "postback",
    "title": "BUTTON_TITLE",
    "payload": "USER"
}]

BUTTON_URL = {
    "type": "web_url",
    "url": "URL",
    "title": "BUTTON_TITLE"
}


def handle_postback(message):
    keyword = message["postback"]["payload"]
    if keyword == "mensa":
        all_mensa(message)
    if keyword == "info":
        info(message)
    elif keyword == "aulastudio":
        all_aulastudio(message)
    elif keyword == "biblioteca":
        all_biblioteca(message)
    elif keyword.startswith("menu"):
        send_menu(message, keyword[4:])
    elif keyword.startswith("daula"):
        send_aula(message, keyword[5:])
    elif keyword.startswith("biblio"):
        send_biblio(message, keyword[6:])
    else:
        pass


def info(message):
    pass
    reply = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "text": "hello, world!"
        }
    }
    text = "Bot NON ufficiale dell'Università di Padova. I dati potrebbero essere incompleti o mancanti: vengono processati automaticamente e non sempre sono aggiornati."
    reply["message"]["text"] = text
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()
    text = "Per qualunque necessità, contatta Michele Colombo qua su Messenger (https://m.me/mikexine) oppure via email a mikexine@gmail.com.\nCiao!"
    reply["message"]["text"] = text
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()


def handle_text(message):
    reply = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Mensa",
                            "subtitle": "Informazioni sulle mense",
                            "image_url": "http://imgur.com/B2Orrys.jpg",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "InfoMensa!",
                                    "payload": "mensa"
                                }
                            ]
                        },
                        {
                            "title": "Aula Studio",
                            "subtitle": "Informazioni sulle aule studio",
                            "image_url": "http://i.imgur.com/Sq8eZlp.jpg",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "InfoAula!",
                                    "payload": "aulastudio"
                                }
                            ]
                        },
                        {
                            "title": "Biblioteca",
                            "subtitle": "Informazioni sulle biblioteche",
                            "image_url": "http://i.imgur.com/PQRYHKl.jpg",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "InfoBiblio!",
                                    "payload": "biblioteca"
                                }
                            ]
                        },
                        {
                            "title": "UnipdBot",
                            "subtitle": "Informazioni su questo bot",
                            "image_url": "http://i.imgur.com/Wmeu4e5.png",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "InfoBot",
                                    "payload": "info"
                                }
                            ]
                        },
                    ]
                }
            }
        }
    }

    print reply
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()



def all_mensa(message):
    reply = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                    ]
                }
            }
        }
    }
    mensaDict = requests.get(API_URL + "mensa/", headers=HEADERS).json()
    del mensaDict["last_update"]
    for m in mensaDict:
        cal = mensaDict[m]["calendario"]
        mensa_el = {
            "title": "Title",
            "subtitle": "Subtitle",
            "buttons": [{
                "type": "postback",
                "title": "BUTTON_TITLE",
                "payload": "USER"
            }]
        }
        if cal["pranzo"] == 1 or cal["cena"] == 1:
            if cal["pranzo"] == 1 and cal["cena"] == 1:
                txt = "Aperta sia a pranzo che a cena: "
            elif cal["pranzo"] == 1 and not cal["cena"] == 1:
                txt = "Aperta solo a pranzo: "
            elif cal["cena"] == 1 and not cal["pranzo"] == 1:
                txt = "Aperta solo a cena: "
            item_title = mensaDict[m]["nome"]
            item_subtitle = mensaDict[m]["orari"]
            btn_title = "Menu"
            btn_payload = "menu" + m
            mensa_el["title"] = item_title
            mensa_el["subtitle"] = txt + item_subtitle
            mensa_el["buttons"][0]["title"] = btn_title
            mensa_el["buttons"][0]["payload"] = btn_payload
            reply["message"]["attachment"]["payload"]["elements"].append(mensa_el)
    print reply
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply))


def send_menu(message, mensa):
    reply = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "text": "hello, world!"
        }
    }
    menuDict = requests.get(API_URL + "mensa/" + mensa, headers=HEADERS).json()['menu']
    if menuDict['primo'][0] == "Menu non pubblicato su www.esupd.gov.it/":
        reply["message"]["text"] = "Menu non pubblicato su www.esupd.gov.it/"
        print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()
    elif menuDict['primo'][0] == "Niente menu, errore su www.esupd.gov.it/":
        reply["message"]["text"] = "Niente menu, errore su www.esupd.gov.it/"
        print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()
    else:
        primo = ', '.join(menuDict['primo'])
        primo = primo.replace(' ,', ',')
        primo = "PRIMO: \n" + primo
        reply["message"]["text"] = primo
        print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()

        secondo = ', '.join(menuDict['secondo'])
        secondo = secondo.replace(' ,', ',')
        secondo = "SECONDO: \n" + secondo
        reply["message"]["text"] = secondo
        print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()

        contorno = ', '.join(menuDict['contorno'])
        contorno = contorno.replace(' ,', ',')
        contorno = "CONTORNO: \n" + contorno
        reply["message"]["text"] = contorno
        print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()

        dessert = ', '.join(menuDict['dessert'])
        dessert = dessert.replace(' ,', ',')
        dessert = "DESSERT: \n" + dessert
        reply["message"]["text"] = dessert
        print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()




def all_aulastudio(message):
    reply = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                    ]
                }
            }
        }
    }
    aulaDict = requests.get(API_URL + "aulastudio/", headers=HEADERS).json()
    for a in aulaDict:
        cal = aulaDict[a]["orari"]
        aula_el = {
            "title": "Title",
            "subtitle": "Subtitle",
            "buttons": [{
                "type": "postback",
                "title": "BUTTON_TITLE",
                "payload": "USER"
            }]
        }
        today = str(datetime.datetime.today().weekday())
        if cal[today] != "":
            item_title = aulaDict[a]["nome"]
            item_subtitle = "Orari di oggi: " + cal[today]
            btn_title = "Dettagli"
            btn_payload = "daula" + a
            aula_el["title"] = item_title
            aula_el["subtitle"] = item_subtitle
            aula_el["buttons"][0]["title"] = btn_title
            aula_el["buttons"][0]["payload"] = btn_payload
            reply["message"]["attachment"]["payload"]["elements"].append(aula_el)
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply))


def send_aula(message, aula):
    reply = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "text": "hello, world!"
        }
    }
    aulaDict = requests.get(API_URL + "aulastudio/" + aula, headers=HEADERS).json()
    text = "Posti: " + aulaDict["posti"]
    text = text + "\nIndirizzo: " + aulaDict["indirizzo"]
    text = text + "\nTelefono: " + aulaDict["tel"]
    reply["message"]["text"] = text
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()
    text = "Calendario completo: " + aulaDict["orario"]
    reply["message"]["text"] = text
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()


def all_biblioteca(message):
    reply_one = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                    ]
                }
            }
        }
    }
    reply_two = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                    ]
                }
            }
        }
    }
    biblioDict = requests.get(API_URL + "biblioteca/", headers=HEADERS).json()
    i = 0
    for b in biblioDict:
        if i < 8:
            print b
            cal = biblioDict[b]["orari"]
            biblio_el = {
                "title": "Title",
                "subtitle": "Subtitle",
                "buttons": [{
                    "type": "postback",
                    "title": "BUTTON_TITLE",
                    "payload": "USER"
                }]
            }
            today = str(datetime.datetime.today().weekday())
            if cal[today] != "":
                item_title = biblioDict[b]["nome"]
                item_subtitle = "Orari di oggi: " + cal[today]
                btn_title = "Dettagli"
                btn_payload = "biblio" + b
                biblio_el["title"] = item_title
                biblio_el["subtitle"] = item_subtitle
                biblio_el["buttons"][0]["title"] = btn_title
                biblio_el["buttons"][0]["payload"] = btn_payload
                reply_one["message"]["attachment"]["payload"]["elements"].append(biblio_el)
        else:
            cal = biblioDict[b]["orari"]
            biblio_el = {
                "title": "Title",
                "subtitle": "Subtitle",
                "buttons": [{
                    "type": "postback",
                    "title": "BUTTON_TITLE",
                    "payload": "USER"
                }]
            }
            today = str(datetime.datetime.today().weekday())
            if cal[today] != "":
                item_title = biblioDict[b]["nome"]
                item_subtitle = "Orari di oggi: " + cal[today]
                btn_title = "Dettagli"
                btn_payload = "biblio" + b
                biblio_el["title"] = item_title
                biblio_el["subtitle"] = item_subtitle
                biblio_el["buttons"][0]["title"] = btn_title
                biblio_el["buttons"][0]["payload"] = btn_payload
                reply_two["message"]["attachment"]["payload"]["elements"].append(biblio_el)
        i += 1
    # print reply_one
    print reply_two
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply_one)).json()
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply_two)).json()



def send_biblio(message, biblio):
    pass
    reply = {
        "recipient": {
            "id": message["sender"]["id"]
        },
        "message": {
            "text": "hello, world!"
        }
    }
    biblioDict = requests.get(API_URL + "biblioteca/" + biblio, headers=HEADERS).json()
    text = biblioDict['nome'] + "\n"
    if biblio == "metelli" or biblio == "pinali":
        text += "Posti liberi: " + biblioDict['posti'] + "\n"
    elif biblio == "bibliogeo":
        text += "Posti liberi: " + biblioDict['posti'] + "\n"
        text += "Notebook liberi: " + biblioDict['notebook'] + "\n"
    else:
        text += ""
    text += "Indirizzo: " + biblioDict["indirizzo"]
    reply["message"]["text"] = text
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()
    text = "Calendario completo: " + biblioDict["orario"]
    reply["message"]["text"] = text
    print requests.post(FB_URL, headers=HEADERS, data=json.dumps(reply)).json()



class fbUnipdbot:

    def __init__(self):
        pass

    def replier(self, incoming_message):
        for entry in incoming_message["entry"]:
            for message in entry["messaging"]:
                if "message" in message:
                    print message
                    print "received text message"
                    handle_text(message)
                if "postback" in message:
                    print "received postback message"
                    handle_postback(message)


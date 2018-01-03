import json
import requests
import time
import urllib
import mbitcoin

TOKEN = '545654541:AAF3-vBMgP-CtfG2qTqaIPltIUdQIcywcOg'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf-8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# {
#     "ok": true,
#     "result": [{
#             "update_id": 625407400,
#             "message": {
#                 "message_id": 1,
#                 "from": {
#                     "id": 24860000,
#                     "first_name": "Gareth",
#                     "last_name": "Dwyer (sixhobbits)",
#                     "username": "sixhobbits"
#                 },
#                 "chat": {
#                     "id": 24860000,
#                     "first_name": "Gareth",
#                     "last_name": "Dwyer (sixhobbits)",
#                     "username": "sixhobbits",
#                     "type": "private"
#                 },
#                 "date": 1478087433,
#                 "text": "/start",
#                 "entities": [{ "type": "bot_command", "offset": 0, "length": 6 }]
#             }
#         }
#     ]
# }
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates['result'])
    last_update = num_updates - 1
    text = updates['result'][last_update]['message']['text']
    chat_id = updates['result'][last_update]['message']['chat']['id']
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            #send_message(text, chat)
            return (text, chat)
        except Exception as e:
            print(e)


def comandos_messages(texto, chat):
    if texto == '/start':
        mensagem = 'Bem vindo ao bot de preços, digite a moeda que você quer monitorar'
        send_message(mensagem, chat)


def getMoeda(texto, chat_id):
    if texto.lower() == 'ltc':
        return 'LTC'
    elif texto.lower() == 'btc':
        return 'BTC'
    else:
        send_message('Não entendi, por favor repita', chat_id)


def main():
    last_update_id = None
    print('começando')
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            texto, chat_id = echo_all(updates)
            if texto == '/start':
                comandos_messages(texto, chat_id)
            elif texto != "":
                coin = getMoeda(texto, chat_id)
                if coin != None:
                    send_message(mbitcoin.retornaHoraValor(
                        mbitcoin.url, coin, mbitcoin.method), chat_id)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

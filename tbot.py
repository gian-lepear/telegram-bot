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
            # send_message(text, chat)
            return (text, chat)
        except Exception as e:
            print(e)


def comandos_messages(texto, chat):
    if texto == '/start':
        # mensagem = 'Bem vindo ao bot de preços, digite a moeda que você quer monitorar: \n\'BTC\' para Bitcoin \n\'LTC\' para Litecoin'
        mensagem2 = 'Menu digite:\n1- Para perguntar o preço\n2-Para monitor o preço'
        send_message(mensagem2, chat)


def getMoedaPreco(chat_id):
    last_update_id = None
    coin = None
    updates = get_updates(last_update_id)
    if len(updates["result"]) > 0:
        last_update_id = get_last_update_id(updates) + 1
        send_message(
            'Digite:\nLitecoin ou LTC para Litecoins\nBitecoin ou BTC para Bitecoins', chat_id)
        time.sleep(10)
        texto, chat_id = echo_all(updates)
        if texto.lower() == 'ltc' or texto.lower() == 'litecoin':
            coin = 'LTC'
        elif texto.lower() == 'btc' or texto.lower() == 'bitecoin':
            coin = 'BTC'
        else:
            send_message(
                'Não entendi, por favor repita. \nDigite: \n\'BTC\' para Bitcoin \n\'LTC\' para Litecoin', chat_id)
        if coin != None:
            resposta, data, coin, last_value = mbitcoin.retornaHoraValor(
                mbitcoin.url, coin, mbitcoin.method)
            send_message(resposta, chat_id)


def monitoraMoeda(moeda):
    pass


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
        #     elif texto != "":
        #         coin = getMoeda(texto, chat_id)
        #         if coin != None:
            if texto == '1':
                getMoedaPreco(chat_id)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

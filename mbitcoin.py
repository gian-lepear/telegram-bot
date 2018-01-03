import requests
import json
import datetime


def retornaHoraValor(url, coin, method):
    url = "{}/{}/{}".format(url, coin, method)
    r = requests.get(url)
    json_data = r.json()
    data = json_data['ticker']['date']
    last_value = json_data['ticker']['last']
    return (data, last_value)


def intToDatetime(dataInt):
    return datetime.datetime.fromtimestamp(dataInt)


def imprimeDataValor(data, coin, valor):
    return 'Data-Hora: {}\nValor do {}: {} R$'.format(data.strftime("%d/%m/%Y %H:%M:%S"), coin, valor)

# import mbitcoin as mb

# url = 'https://www.mercadobitcoin.net/api'
# coin = 'LTC'
# method = 'ticker'

# data, last_value = retornaHoraValor(url, coin, method)
# data = intToDatetime(data)
# texto = imprimeDataValor(data, coin, last_value)
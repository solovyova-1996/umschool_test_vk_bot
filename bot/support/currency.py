import requests
import urllib.request
from xml.dom import minidom
from config import currency_api
from decimal import Decimal

currency_name = {"USD": "Доллар США", "EUR": "Евро", "JPY": "Японская иена", "GBP": "Британский фунт стерлингов",
                 "AUD": "Фвстралийский доллар", }


def get_request_currency(currency):
    result = requests.get("https://api.apilayer.com/fixer/latest",
                          params={'symbols': "RUB", 'base': currency, 'apikey': currency_api})
    data = result.json()
    if data is not None:
        return f"1 {currency_name[data['base']]}({data['base']}) - {data['rates']['RUB']}₽\n"
    else:
        raise AttributeError


def get_currency_api():
    result = "Топ 5 валют мира:\n"
    for currency in currency_name:
        try:
            result_currency = get_request_currency(currency)
            result += result_currency
        except AttributeError:
            pass
    return result


def get_currency():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"

    webFile = urllib.request.urlopen(url)
    data = webFile.read()
    with open("currency.xml", "wb") as localFile:
        localFile.write(data)
    webFile.close()
    doc = minidom.parse("currency.xml")

    currency = doc.getElementsByTagName("Valute")

    result = "Топ 5 валют мира:\n"
    for rate in currency:
        charcode = rate.getElementsByTagName("CharCode")[0]
        name = rate.getElementsByTagName("Name")[0]
        value = rate.getElementsByTagName("Value")[0]
        value = float(str(value.firstChild.data).replace(",", "."))
        if charcode.firstChild.data in ["EUR", "USD", "JPY", "GBP", "AUD"]:
            result += f"1 {name.firstChild.data} ({charcode.firstChild.data}) - {Decimal(value).quantize(Decimal('1.00'))} ₽\n"
    return result

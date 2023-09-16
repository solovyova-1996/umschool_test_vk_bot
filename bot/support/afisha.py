import requests
from bs4 import BeautifulSoup
from transliterate import translit
import json


def get_afisha(city, day_from_user):
    day_dict = {"Сегодня": "na-segodnya", "Завтра": "na-zavtra"}
    result_string = f"Aфиша событий ({day_from_user}-{city}):\n"
    city_update = translit(city, language_code='ru', reversed=True).lower()
    toggle = day_dict[day_from_user]
    url = f"https://www.afisha.ru/{city_update}/events/{toggle}/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup_el_body = soup.find('script', attrs={"data-test": "JSONLD-MICRODATA"})
    result = json.loads(soup_el_body.text).get("itemListElement")

    for item in enumerate(result[:5], 1):
        try:
            name = item[1].get('item').get('name') if item[1].get('item').get('name') is not None else ""

            if 'offers' in item[1].get('item') and 'price' in item[1].get('item').get('offers'):
                price = item[1].get('item').get('offers').get('price')
            else:
                price = "Цена не указана"
            if 'offers' in item[1].get('item') and 'priceCurrency' in item[1].get('item').get('offers'):
                currency = item[1].get('item').get('offers').get('priceCurrency')
            else:
                currency = ""
            url = item[1].get('item').get('url') if item[1].get('item').get('url') is not None else ""
            str_res = f"{item[0]}.{name}\n{price} {currency}\nhttps://www.afisha.ru{url}\n"
        except AttributeError:
            str_res = ""
        result_string += str_res
    return result_string

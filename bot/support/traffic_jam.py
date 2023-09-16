import requests
from bs4 import BeautifulSoup


def get_soup(city):
    url = 'https://www.rush-analytics.ru/blog/spisok-regionov-yandeksa'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup_el_body = soup.find('div', class_='content-area')

    soup_result_animals = soup_el_body.find_all("p")

    for item in soup_result_animals:
        if "глобальный" in str(item).lower() and city.lower() in str(item).lower():
            res = list(str(item)[3:-4].split("—"))
            if res[1].lstrip().rstrip() == city:
                return int(res[-1])


def get_traffic_jam(city):
    region_id = get_soup(city)
    if region_id is None:
        return None
    else:
        url_traffic = f"https://export.yandex.ru/bar/reginfo.xml?region={region_id}"
        page = requests.get(url_traffic)
        return page.text[page.text.find("<tend>") + 6:page.text.find("</tend>")]

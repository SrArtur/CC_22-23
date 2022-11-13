import requests
from config import ID_PENINSULA, URL, HEADERS


def parse_date(date, simplify: bool):
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    date = {"year": year, "month": month, "day": day, "hour": hour} if not simplify else {"day": day, "hour": hour}
    return date


def convert_to_kwh(price):
    """
    Hace la conversión de MWh a KWh.

    :param price: Precio en MWh.
    :return: Precio en KWh.
    """
    return round((price / 1000), 5)


def get_today_prices():
    """
    Obtiene los precios del día en transcurso. A partir de las 20:00 horas en España
    son los precios del día siguiente.
    :return: prices: precios del día.
    """
    response = requests.get(url=URL, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        prices = [(parse_date(x['datetime']), convert_to_kwh(x['value'])) for x in data['indicator']['values'] if
                  x['geo_id'] == ID_PENINSULA]

    return prices

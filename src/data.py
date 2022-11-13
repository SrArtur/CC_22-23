import requests
from config import ID_PENINSULA, URL, HEADERS


def parse_date(date):
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    date = {"year": year, "month": month, "day": day, "hour": hour}
    return date


def convert_to_kwh(price):
    """
    Hace la conversión de MWh a KWh.

    :param price: Precio en MWh.
    :return: Precio en KWh.
    """
    return round((price / 1000), 5)


def get_today_prices(db_format: bool, ):
    """
    Obtiene los precios del día en transcurso. A partir de las 20:00 horas en España
    son los precios del día siguiente.

    :param db_format: Si se desea el tipado de los datos para almacenar en la base de datos
    :return: prices: precios del día.
    """
    response = requests.get(url=URL, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        prices = [(parse_date(x['datetime']), convert_to_kwh(x['value'])) for x in
                  data['indicator']['values'] if
                  x['geo_id'] == ID_PENINSULA]

        if db_format:
            res = dict()
            hours = dict()
            for p in prices:
                year = str(p[0]['year'])
                month = str(p[0]['month'])
                day = str(p[0]['day'])
                hour = str(p[0]['hour'])
                price = p[1]
                hours[hour] = price
            res[day + month + year] = hours
            prices = res

    return prices

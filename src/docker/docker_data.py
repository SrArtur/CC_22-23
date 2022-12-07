import requests
from src.docker.config import ID_PENINSULA, URL, HEADERS
import datetime


def today_day():
    """
    Obtiene el día de hoy con el formato almacenado en la base de datos.
    :return: Dia en formato [dia][mes][año]
    """
    today = datetime.datetime.now()
    return str(today.day) + str(today.month) + str(today.year)


def parse_date(date, simplify: bool = False):
    """
    Cambia el formato de la fecha obtenida desde la API.
    El formato puede ser: {año,mes,dia,hora} ó {mes, dia, hora} si simplify
    :param date: Fecha
    :param simplify: Flag para simplificar la fecha para el usuario.
    :return: Fecha en el formato indicado
    """
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    date = {"year": year, "month": month, "day": day, "hour": hour} if not simplify else {"month": month, "day": day,
                                                                                          "hour": hour}
    return date


def convert_to_kwh(price):
    """
    Hace la conversión de MWh a KWh.
    :param price: Precio en MWh.
    :return: Precio en KWh.
    """
    return round((price / 1000), 5)


def get_today_prices(db_format: bool = True, simplify: bool = False):
    """
    Obtiene los precios del día en transcurso. A partir de las 20:00 horas en España
    son los precios del día siguiente.
    :param simplify: Si se desea el formato más simplificado. Sólo horas y precios.
    :param db_format: Si se desea el tipado de los datos para almacenar en la base de datos.
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
            prices = hours if simplify else res
    return prices


def average_price(day: str = None, verbose: bool = False):
    """
    Calcula la media de los precios para el día especificado.
    En el caso de que no se proporcione día se sobreentiende
    que es el actual.
    :param verbose: Si se desea imprimir por pantalla
    :param day:
    :return: Precio medio del día
    """
    if day is None:
        prices = get_today_prices(simplify=True)
        arg = "hoy"
    avg = round(sum([price for (hour, price) in prices.items()]) / len(prices), 4)
    if verbose:
        print(f"La media de {arg} es {avg}")
    return avg


def minimum_prices(day: str = None):
    """
    Obtiene el y los precios más baratos del día. En el caso
    de que no se proporcione día se sobreentiende que es el
    actual.
    :param day: Día a consultar
    :return: precios y precio más baratos.
    """

    if day is None:
        prices = get_today_prices(simplify=True)
        arg = "hoy"

    avg = average_price(day)
    minimum_p = {hour: round(price, 4) for hour, price in sorted(prices.items(), key=lambda item: item[1]) if
                 price <= avg}
    print(f"Los precios mínimos de {arg} es {minimum_p}")
    minimum = list(minimum_p.items())[0]

    print(f"El precio mínimo es a las {minimum[0]} con {minimum[1]}")
    return minimum_p, minimum


def classify_prices(day: str = None):
    """
    Clasifica los precios en valle,llano y punta.
    En el caso de que no se proporcione día se
    sobreentiende que es el actual.
    :param day: Día a consultar.
    :return: La clasificación de los precios.
    """
    if day is None:
        prices = get_today_prices(simplify=True)

    avg = average_price(day)
    classification = {"valle": {}, "llano": {}, "punta": {}}

    for (hour, price) in prices.items():
        if price < avg - 0.01:
            classification["valle"][hour] = price
        elif avg - 0.01 <= price <= avg + 0.01:
            classification["llano"][hour] = price
        else:
            classification["punta"][hour] = price

    return classification


if __name__ == '__main__':
    print(f"El día de hoy es {today_day()}\n")
    print(f"Precios de hoy: {get_today_prices()}\n")
    average_price(verbose=True)
    print()
    minimum_prices()
    print()
    print("La clasificación de los precios: ", classify_prices())

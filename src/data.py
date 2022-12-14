import datetime
import time
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, interp1d
import numpy as np
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists

from src.LightPrices import LightPrices
from src.config import ID_PENINSULA, URL, HEADERS, DB_URI, DB_NAME


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

    prices = get_prices(today_day())
    if prices is not None:
        print("La consulta es a la base de datos.")
    else:
        print("La consulta es a la API.")
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
                save_prices(res)
                prices = hours if simplify else res

    return prices


def save_prices(prices: dict):
    """
    Almacena en la base de datos los precios que recibe como atributo.
    :param prices: Diccionario con los precios del día de hoy.
    :return: None
    """

    if not database_exists(DB_URI + "/" + DB_NAME):
        engine = create_engine(DB_URI, echo=True)
        engine.execute("CREATE DATABASE  {0}".format(DB_NAME))  # create db
        print("Bases de dato creada.")
    data = LightPrices()
    # TODO Mejora la forma adaptada a la bd
    data.day = list(prices.keys())[0]
    data.day_prices = list(prices.values())[0]
    if get_prices(data.day) is None:
        print(f"Se han almacenado los precios del día {data.day}")
        engine = create_engine(DB_URI + "/" + DB_NAME, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        LightPrices.metadata.create_all(engine)
        session.add(data)
        session.commit()
    else:
        print(f"Los precios de {data.day} ya están almacenados.")


def get_prices(day: str):
    """
    Consulta el precio de la luz el día especificado por parámetros.
    :param day: Día a consultar.
    :return: Diccionario con los precios del día especificados en day
    """
    try:
        engine = create_engine(DB_URI + "/" + DB_NAME)
        Session = sessionmaker(bind=engine)
        session = Session()
        q = session.query(LightPrices).get(day)
        return q.day_prices
    except AttributeError:
        print("La fecha solicitada no está disponible o el formato de fecha es incorrecto.")


def average_price(day: str = None):
    """
    Calcula la media de los precios para el día especificado.
    En el caso de que no se proporcione día se sobreentiende
    que es el actual.
    :param day:
    :return: Precio medio del día
    """
    if day is None:
        prices = get_today_prices(simplify=True)
        arg = "hoy"
    else:
        prices = get_prices(day)
        arg = "del día " + day
    avg = round(sum([price for (hour, price) in prices.items()]) / len(prices), 4)
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
    else:
        prices = get_prices(day)
        arg = "del día " + day

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
    else:
        prices = get_prices(day)

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


def activation(current_hour: str = datetime.datetime.now().hour, minutes: int = datetime.datetime.now().minute):
    """
    Envía la señal de activación al dispositivo. En el caso de que no se establezca hora de activación, usará la actual.
    En el caso, de que la hora no sea una de las más baratas, esperá hasta la siguiente hora más barata del mismo día.

    :param current_hour: Hora especificada por el usuario o por defecto la actual
    :param minutes: Minutos especificada por el usuario o por defecto el actual
    :return: Señal de activación

    """
    min_prices, _ = minimum_prices()
    activate = False
    rest = None
    current_hour = "0" + current_hour if len(current_hour) == 1 else current_hour

    if current_hour in min_prices:
        activate = True
        print("Dispositivo activado.")
        print(f"El precio del kwh actualmente es de {min_prices[current_hour]} ")
    else:
        for hour in min_prices.keys():
            if int(current_hour) < int(hour):
                rest = datetime.timedelta(hours=int(hour), minutes=0) - datetime.timedelta(hours=int(current_hour),
                                                                                           minutes=int(minutes))
                print(f"El dispositivo se activará dentro de {rest.seconds} segundos")
                # time.sleep(rest.seconds)
                time.sleep(3)
                activate = True
                print(f"El precio del kwh actualmente es de {min_prices[hour]} ")
                print("Dispositivo activado.")
                # La idea es activar la función del SDK de Alexa y/o Google Home.
                break
        if not rest:
            print("Una hora más barata será al día siguiente")

    return activate


def view_price(day: str = today_day(), trend: bool = False):
    """
    Representa gráficamente la evolución del precio a lo largo del día especificado
    en day. En caso de que no se especifique, se sobreentiendo el día actual.

    :param day: Día a representar
    :param trend: Si se desea ver la tendencia global en vez del día
    :return: None
    """

    prices = get_prices(day)
    prices = [dict([int(a), float(x)] for a, x in prices.items())]
    prices = prices[0].items()

    x, y = zip(*prices)
    x = np.asarray(x)
    y = np.asarray(y)
    interpolate = interp1d(x, y, kind="cubic")
    x = np.linspace(x.min(), x.max(), 200)
    y = interpolate(x)

    plt.figure(figsize=(10, 6))

    if trend:
        ax = plt.gca()
        ax.set_ylim([0, y.max() + 0.1])

    title = "Evolución del precio. Día " + day
    plt.title(title)
    plt.xlabel("Hora")
    plt.ylabel("Precio (céntimos)")
    plt.plot(x, y)
    plt.show()

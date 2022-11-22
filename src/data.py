import requests
from src.config import ID_PENINSULA, URL, HEADERS, DB_URI, DB_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from src.LightPrices import LightPrices
import datetime


def today_day():
    today = datetime.datetime.now()
    return str(today.day) + str(today.month) + str(today.year)


def parse_date(date, simplify: bool = False):
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

    :param db_format: Si se desea el tipado de los datos para almacenar en la base de datos
    :return: prices: precios del día.
    """
    # TODO Almecenar los datos al hacer la primera llamada.
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


def save_prices(prices: dict):
    if not database_exists(DB_URI + "/" + DB_NAME):
        engine = create_engine(DB_URI, echo=True)
        engine.execute("CREATE DATABASE  {0}".format(DB_NAME))  # create db
        print("Bases de dato creada.")
    data = LightPrices()
    # TODO Mejora la forma adaptada a la bd
    data.day = list(prices.keys())[0]
    data.day_prices = list(prices.values())[0]
    if get_prices(data.day) is None:
        engine = create_engine(DB_URI + "/" + DB_NAME, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        LightPrices.metadata.create_all(engine)
        session.add(data)
        session.commit()
    else:
        print(f"Los precios de {data.day} ya están almacenados.")


def get_prices(day: str):
    try:
        engine = create_engine(DB_URI + "/" + DB_NAME)
        Session = sessionmaker(bind=engine)
        session = Session()
        q = session.query(LightPrices).get(day)
        return q.day_prices
    except AttributeError:
        print("La fecha solicitada no está disponible o el formato de fecha es incorrecto.")

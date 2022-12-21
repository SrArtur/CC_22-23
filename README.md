# :brain: **SmartGrid** :electric_plug:

Bienviendo a la página principal del proyecto **SmartGrid** para la asignatura de *Cloud Computing* del Máster de
Ingeniería Informático de la Universidad de Granada

<img title="" src="docs/img/logo.png" alt="" data-align="center" width="120">

El estado actual del proyecto puede ver en [Milestones](https://github.com/SrArtur/CC_22-23/milestones) y en el **nuevo
apartado** [Estado del proyecto](#estado-del-proyecto)

---

## Enlaces de interés

En la documentación del proyecto podemos encontrar actualmente la siguiente información:

- [Configuración de git y Github.](https://github.com/SrArtur/CC_22-23/blob/main/docs/configuration.md)

- [Descripción del proyecto.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hio0.md)

- [Planificación del proyecto.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito1.md)

- [Test.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito2.md)

- [Creación de un contenedor para pruebas.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito3.md)

- [Integración Continua](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito4.md)

----

[![Build Status](https://app.travis-ci.com/SrArtur/CC_22-23.svg?branch=main)](https://app.travis-ci.com/SrArtur/CC_22-23)
[![CircleCI](https://circleci.com/gh/SrArtur/CC_22-23.svg?style=svg)](https://app.circleci.com/pipelines/github/SrArtur/CC_22-23)
## HITO 4 - Integración Continua

Para la realización de este hito se ha seguido con detalle la documentación
de [Cuarto HIto: Integración Continua](http://jj.github.io/CC/documentos/proyecto/4.CI.html).

## Integración Continua con Travis

La elección de Travis viene justificada por familiaridad y fácil integración en el proyecto. Para ello se ha seguido
la [guía de inicio](https://docs.travis-ci.com/user/tutorial/#to-get-started-with-travis-ci-using-github) que
proporciona la propia plataforma. El primer paso es darse de alta en la plataforma y sincronizar con la cuenta de
Github,así como con todos los repositorios, para futuros usos si es necesario (este proceso tarda un poco por la
comunicación con Github).

Una vez completado el proceso, se deben ver los repositorios de tu cuenta en el menú de la izquierda. Para habilitar la
integración continua, es necesario seleccionar un plan. En el caso de este proyecto se ha seleccionado el *Trial Plan*,
ya que cumple de sobra los requisitos. Una vez finalizado este proceso, se pueden ver los créditos gratis que
proporciona Travis, así como los usados hasta el momento (véase la siguiente figura). Es a partir de este momento,
cuando ya tenemos la Integración Continua habilitada y es entonces, a partir del primer *push* a nuestro proyecto,
cuando comenzará.

![](/docs/img/creditos.png)

El archivo de configuración de Travis tienen el siguiente contenido:
```yaml
language: python
python:
  - "3.8"
  - "3.9"
install:
  - pip install -r requirements.txt
script:
  - python -m unittest discover src/docker/test
```

## Resultados obtenidos

En este caso, en el primer intento, no se consiguió la integración debido a dos motivos:

- <u>Incompatibilidad del módulo `iso8601`  y la versión 3.7 de Python</u>. Como consecuencia, hasta buscar una
  alternativa, queda deshabilitada esta versión de Python del proyecto.

- <u>Variables de entorno no configuradas.</u> Para mantener a salvo elementos tan críticos como el token de la API o la
  forma de acceder a la base de datos, es necesario configurar las variables de entorno. En este caso, se hizo uso de
  Github Secrets para ello.

![](/docs/img/test_fail.png)

Una vez solventados ambos problemas, los test pasan correctamente y ya tenemos integración continua en el proyecto, como
se puede apreciar
en  [![Build Status](https://app.travis-ci.com/SrArtur/CC_22-23.svg?branch=main)](https://app.travis-ci.com/SrArtur/CC_22-23)
y en las siguientes figuras.

![](/docs/img/test_passing.png)

# Integración continua con CircleCI

Como alternativa gratuita a Travis, de manera complementaria se ha decidido usar CircleCI. La configuración ha sido muy similar a Travis, aunque el contenido de la plantilla difiere (Travis simplifica y da por hecho contenido que no es especificado). Su contenido es el siguiente:
````yaml
version: 2.1
orbs:
  python: circleci/python@1.5.0
jobs:
  build-and-test:
    docker:
      - image: cimg/python:3.9.2
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
      - run:
          name: Run tests
          command: python -m unittest discover src/docker/test

workflows:
  sample: 
    jobs:
      - build-and-test
````
De la misma forma, al hacer `push`, se pasan los test. El resultado obtenido se puede ver en la siguiente figura aunque también en el _badge_ [![CircleCI](https://circleci.com/gh/SrArtur/CC_22-23.svg?style=svg)](https://app.circleci.com/pipelines/github/SrArtur/CC_22-23):

![](/docs/img/circleci.png)

# Estado del proyecto :chart_with_upwards_trend:

A lo largo de la sucesión de los diferentes hitos de la asignatura, de manera paralela, se ha ido desarrollando código
con el que se ha conseguido entre otros objetivos:

- **Mostrar los precios de hoy** (referentes al 21 de Diciembre de 2022):

```json
{
  '00': 0.10505,
  '01': 0.09467,
  '02': 0.08396,
  '03': 0.08082,
  '04': 0.0806,
  '05': 0.09526,
  '06': 0.1004,
  '07': 0.10317,
  '08': 0.14127,
  '09': 0.14383,
  '10': 0.18247,
  '11': 0.1624,
  '12': 0.16125,
  '13': 0.15986,
  '14': 0.11008,
  '15': 0.11696,
  '16': 0.13295,
  '17': 0.14849,
  '18': 0.20342,
  '19': 0.20925,
  '20': 0.21284,
  '21': 0.20493,
  '22': 0.13229,
  '23': 0.12229
}
```

- **Mostrar los precios de _cualquier_ día** (referentes al 17 de Diciembre de 2022)

```json
{
  '00': 0.26835,
  '01': 0.27927,
  '02': 0.2849,
  '03': 0.28072,
  '04': 0.28241,
  '05': 0.28505,
  '06': 0.28181,
  '07': 0.24923,
  '08': 0.25343,
  '09': 0.25165,
  '10': 0.2304,
  '11': 0.22588,
  '12': 0.22316,
  '13': 0.21906,
  '14': 0.20781,
  '15': 0.21082,
  '16': 0.22949,
  '17': 0.24474,
  '18': 0.26244,
  '19': 0.26311,
  '20': 0.26308,
  '21': 0.25414,
  '22': 0.23954,
  '23': 0.21826
}
```

- **Precio medio de hoy** (referentes al 21 de Diciembre de 2022)

```json
"La media de hoy es 0.137"
```

- **Precio medio de _cualquier_ día**

```json
"La media de del día 17122022 es 0.2504"
```

- **Precio mínimo de hoy** (referentes al 21 de Diciembre de 2022)

```json
"El precio mínimo es a las 04 con 0.0806"
```

- **Precio minimo de _cualquier_ día**

```json
"El precio mínimo es a las 14 con 0.2078"
```

- **Clasificación de precios de hoy** (referentes al 21 de Diciembre de 2022)

```json
{
  'valle': {
    '00': 0.10505,
    '01': 0.09467,
    '02': 0.08396,
    '03': 0.08082,
    '04': 0.0806,
    '05': 0.09526,
    '06': 0.1004,
    '07': 0.10317,
    '14': 0.11008,
    '15': 0.11696,
    '23': 0.12229
  },
  'llano': {
    '08': 0.14127,
    '09': 0.14383,
    '16': 0.13295,
    '22': 0.13229
  },
  'punta': {
    '10': 0.18247,
    '11': 0.1624,
    '12': 0.16125,
    '13': 0.15986,
    '17': 0.14849,
    '18': 0.20342,
    '19': 0.20925,
    '20': 0.21284,
    '21': 0.20493
  }
}

```

- **Clasificación de precios de cualquier día** (referentes al 17 de Diciembre de 2022)

```json
{
  'valle': {
    '10': 0.2304,
    '11': 0.22588,
    '12': 0.22316,
    '13': 0.21906,
    '14': 0.20781,
    '15': 0.21082,
    '16': 0.22949,
    '22': 0.23954,
    '23': 0.21826
  },
  'llano': {
    '07': 0.24923,
    '08': 0.25343,
    '09': 0.25165,
    '17': 0.24474,
    '21': 0.25414
  },
  'punta': {
    '00': 0.26835,
    '01': 0.27927,
    '02': 0.2849,
    '03': 0.28072,
    '04': 0.28241,
    '05': 0.28505,
    '06': 0.28181,
    '18': 0.26244,
    '19': 0.26311,
    '20': 0.26308
  }
}

```

- **Gráfica de la evolución** (referentes a los días 17 y 21 de Diciembre de 2022). A la izquierda se muestra como varía el precio según el máximo y minimo de hoy, en la grafica de la derecha se observa de una manera más global.
![21 de Diciembre](/docs/img/evolucion_precios_ambos.png)
![17 de Diciembre](/docs/img/evolucion_precios_ambos_cualquier.png)

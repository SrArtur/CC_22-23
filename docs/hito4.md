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

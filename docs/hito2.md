# HITO 2 - Test

Este hito tiene el objetivo es añadir test y las tareas necesarias para su ejecución. Se ha seguido con detalle la documentación de [Segundo Hito: Test](http://jj.github.io/CC/documentos/proyecto/2.Tests.html), [Preparando los tests unitarios](https://jj.github.io/curso-tdd/temas/tests-unitarios-organizaci%C3%B3n.html) y [Gestores de tareas y su importancia en automatización del desarrollo

## Gestor de tareas

Como gestor de tareas se ha decidido usar `Make` debido a la familiaridad de uso con él. Ademas es posible usarlo fácilmente tanto en Windows (con WSL) como con Ubuntu. El contenido de `Makefile` es el siguiente:

```makefile
run:
        python -m unittest discover
```

## Biblioteca de aserciones y marco de pruebas

Para las comprobaciones del código se ha decidido usar `unittest` debido a que es el que viene por defecto con Python y por tanto, tiene muy buena integración con este lenguaje así como de los recursos disponibles. `unittest` es tanto marco de prueba como biblioteca de aserciones y está basado en el marco XUnit. Las partes del código testeadas, se describen más abajo.

## YAML

El contenido del fichero YAML es el siguiente. Se especifica el lenguaje, las versiones en que es compatible, así como instalar los requerimientos y ejecutar los test. 

> 

```yaml
language: python
python:
  - "3.7"
  - "3.8"
  - "3.9"
install:
  - pip install -r requirements.txt
script:
  - python -m unittest discover
```

## Partes del código testeadas

Las partes del código testeadas por ahora, son las correspondientes a los avances en el Hito 0. Más concretamente, las llamadas a la API y base datos, así como el formateo  y la conversión de diferentes datos. Los test se pueden encontrar en los siguientes enlaces:

- [Test de datos]()

- [Test de base de datos]()

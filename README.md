# :brain: **SmartGrid** :electric_plug:

Bienviendo a la página principal del proyecto **SmartGrid** para la asignatura de *Cloud Computing* del Máster de Ingeniería Informático de la Universidad de Granada

<img title="" src="docs/img/logo.png" alt="" data-align="center" width="120">

El estado actual del proyecto puede ver en [Milestones](https://github.com/SrArtur/CC_22-23/milestones).

---

## Enlaces de interés

En la documentación del proyecto podemos encontrar actualmente la siguiente información:

- [Configuración de git y Github](https://github.com/SrArtur/CC_22-23/blob/main/docs/configuration.md)

- [Descripción del proyecto](https://github.com/SrArtur/CC_22-23/blob/main/docs/hio0.md).

- [Planificación del proyecto.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito1.md) 

- [Test.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito2.md) (También disponible a continuación)

----

### HITO 2 - Test

Este hito tiene el objetivo es añadir test y las tareas necesarias para su ejecución. Se ha seguido con detalle la documentación de [Segundo Hito: Test](http://jj.github.io/CC/documentos/proyecto/2.Tests.html), [Preparando los tests unitarios](https://jj.github.io/curso-tdd/temas/tests-unitarios-organizaci%C3%B3n.html) y [Gestores de tareas y su importancia en automatización del desarrollo](https://jj.github.io/curso-tdd/temas/gestores-tareas.html)

## Gestor de tareas

Como gestor de tareas se ha decidido usar `Make` debido a la familiaridad de uso con él. Ademas es posible usarlo fácilmente tanto en Windows (con WSL) como con Ubuntu. El contenido de `Makefile` es el siguiente:S

```makefile
run:
        python -m unittest discover
```

## Biblioteca de aserciones y marco de pruebas

Para las comprobaciones del código se ha decidido usar `unittest` debido a que es el que viene por defecto con Python y por tanto, tiene muy buena integración con este lenguaje así como de los recursos disponibles. `unittest` es tanto marco de prueba como biblioteca de aserciones y está basado en el marco XUnit. Las partes del código testeadas, se describen más abajo.

## YAML

El contenido del fichero YAML es el siguiente. Se especifica el lenguaje, las versiones en que es compatible, así como instalar los requerimientos y ejecutar los test (más adelante, ahora mismo es con `Make`.)

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

Las partes del código testeadas por ahora, son las correspondientes a los avances en el Hito 0. Más concretamente, las llamadas a la API y base datos, así como el formateo y la conversión de diferentes datos. Los test se pueden encontrar en los siguientes enlaces:

- [Test de datos](https://github.com/SrArtur/CC_22-23/blob/main/test/test_data.py)

- [Test de base de datos](https://github.com/SrArtur/CC_22-23/blob/main/test/test_database.py)

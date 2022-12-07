# :brain: **SmartGrid** :electric_plug:

Bienviendo a la página principal del proyecto **SmartGrid** para la asignatura de *Cloud Computing* del Máster de
Ingeniería Informático de la Universidad de Granada

<img title="" src="docs/img/logo.png" alt="" data-align="center" width="120">

El estado actual del proyecto puede ver en [Milestones](https://github.com/SrArtur/CC_22-23/milestones).

---

## Enlaces de interés

En la documentación del proyecto podemos encontrar actualmente la siguiente información:

- [Configuración de git y Github.](https://github.com/SrArtur/CC_22-23/blob/main/docs/configuration.md)

- [Descripción del proyecto.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hio0.md)

- [Planificación del proyecto.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito1.md)

- [Test.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito2.md)

- [Creación de un contenedor para pruebas.](https://github.com/SrArtur/CC_22-23/blob/main/docs/hito3.md) (También
  disponible a continuación)

----

## HITO 3 - Creación de un Contenedor para pruebas

Para la realización de esta práctica se ha
consultado [Creación de un contenedor de pruebas](https://jj.github.io/CC/documentos/proyecto/3.Docker) del temario de
la asignatura, además de la documentación de Docker detallada más adelante.

### Elección del contenedor base

Para la creación del `dockerfile` me he basado en la imagen de Python 3.9-slim que a su vez usa de base Debian 10-slim. La elección de esta imagen viene motivada por el poco uso de librerías que hace, únicamente instala las librerías base de Python. Por tanto, se obtiene un contenedor muy liviano de unos 150 MB.

### Dockerfile y buenas prácticas

El `dockerfile` se ha escrito acorde a la documentación de Docker, [_Build your
image_](https://docs.docker.com/language/python/build-images/). Como se ha mencionado previamente, al usar esas imágenes base, apenas tiene programas necesarios instalados, es por ello que en el contenido del fichero se instalan programas necesarios, en este caso, git. El contenido del `dockerfile` es el siguiente:

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
RUN useradd -d /CC_22-23 CC_22-23
RUN apt-get -y update
# Instala git
RUN apt-get -y install git
# Crea el directorio sobre el que va el proyecto
RUN mkdir /CC_22-23
# Concedemos permisos de lectura
RUN chown -R CC_22-23:CC_22-23 /CC_22-23
USER CC_22-23
RUN cd /CC_22-23
# Clona la ultima versión del repositorio
RUN git clone https://github.com/SrArtur/CC_22-23.git
RUN cd /CC_22-23

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
# Ejecuta los test específicos de docker
# En caso de fallos, el contenedor no se construye
RUN [ "python3" , "-m","unittest","discover","src/docker/test"]

CMD [ "python3" , "-m","unittest","discover","src/docker/test"]


```

Como se ha mostrado, se han seguido las buenas prácticas de Docker de la documentación [*Best practices for writing Dockerfiles | Docker Documentation*](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

Para construir el contenedor, el comando y la salida por pantalla es la siguiente:

```shell
C:\Users\aoa2e\Desktop\CC_22-23 > docker build --tag cc_22-23 .
[+] Building 1.7s (22/22) FINISHED
 => [internal] load build definition from Dockerfile                                                               0.0s
 => => transferring dockerfile: 32B                                                                                0.0s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                         0.6s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ce  0.0s
 => [internal] load .dockerignore                                                                                  0.0s
 => [internal] load build definition from Dockerfile                                                               0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim-buster                                          0.6s
 => [internal] load build context                                                                                  0.1s
 => => transferring context: 19.93kB                                                                               0.1s
 => [ 1/14] FROM docker.io/library/python:3.9-slim-buster@sha256:31b159250e058c356685e79a1ee427bb0d632064fe30e440  0.0s
 => CACHED [ 2/14] RUN useradd -d /CC_22-23 CC_22-23                                                               0.0s
 => CACHED [ 3/14] RUN apt-get -y update                                                                           0.0s
 => CACHED [ 4/14] RUN apt-get -y install git                                                                      0.0s
 => CACHED [ 5/14] RUN mkdir /CC_22-23                                                                             0.0s
 => CACHED [ 6/14] RUN chown -R CC_22-23:CC_22-23 /CC_22-23                                                        0.0s
 => CACHED [ 7/14] RUN cd /CC_22-23                                                                                0.0s
 => CACHED [ 8/14] RUN git clone https://github.com/SrArtur/CC_22-23.git                                           0.0s
 => CACHED [ 9/14] RUN cd /CC_22-23                                                                                0.0s
 => CACHED [10/14] COPY requirements.txt requirements.txt                                                          0.0s
 => CACHED [11/14] RUN pip3 install -r requirements.txt                                                            0.0s
 => CACHED [12/14] COPY . .                                                                                        0.0s
 => CACHED [13/14] RUN [ "python3" , "-m","unittest","discover","src/docker/test"]                                 0.0s
 => exporting to image                                                                                             0.1s
 => => exporting layers                                                                                            0.0s
 => => writing image sha256:2229efcf0c99baf0c441097d3b66389de453674ba440ee28f1a28a587c3ab39a                       0.0s
 => => naming to docker.io/library/cc_22-23
```

Consiguiendo que la imagen final apenas ocupe 248 MB, tras instalar los requisitos del programa y git.

Al ejecutar el contendor, debido que está destinado a pruebas, ejecutamos los test, de la siguiente forma:

```bash
C:\Users\aoa2e\Desktop\CC_22-23> docker run cc_22-23
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### Dockerhub

Una vez completamos el `dockerfile` y se ha comprobado su correcto funcionamiento, subimos la imagen a un repositorio propio en Docker Hub. El respositorio es el siguiente:  [Docker Hub - CC-22-23](https://hub.docker.com/repository/docker/srarturo/cc_22-23/general). 

Para subir la imagen:

```shell
C:\Users\aoa2e\Desktop\CC_22-23> docker tag cc_22-23:latest srarturo/cc_22-23:testing
C:\Users\aoa2e\Desktop\CC_22-23> docker push srarturo/cc_22-23:testing
The push refers to repository [docker.io/srarturo/cc_22-23]
93230525d6ce: Pushed
b00639565785: Pushed
20268002c2b7: Pushed
e3daba0ef532: Pushed
b30f8fdf9787: Pushed
b4546b938c54: Pushed
bdb9b94ea761: Pushed
be5fbc64a56c: Pushed
9068fecf772d: Pushed
277ebb90f471: Pushed
97b29271e4e0: Pushed
56ea3231b865: Pushed
f48d51232399: Pushed
5c39890b8729: Pushed
2fa5cbc8f06d: Pushed
4d5f738025a7: Pushed
4c2b77c2cff5: Pushed
testing: digest: sha256:33ff203fd1946f7e033456133f13df2a0f72e2193bc923ced6400484d3887027 size: 3873
```



Para descargar el contenedor: `docker pull srarturo/cc_22-23:base`

> Debido a que mi nombre de usuario en Github (SrArtur) y el de Docker Hub (SrArturo) varían un poco, he incluido DOCKER_HUB_USERNAME

### Registros alternativos

Debido a la falta de tiempo, no ha sido posible completar este apartado para la entrega del hito 3.

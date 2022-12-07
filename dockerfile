# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
RUN useradd -d /CC_22-23 CC_22-23
RUN apt-get -y update
RUN apt-get -y install git
RUN mkdir /CC_22-23
RUN chown -R CC_22-23:CC_22-23 /CC_22-23
USER CC_22-23
RUN cd /CC_22-23
RUN git clone https://github.com/SrArtur/CC_22-23.git
RUN cd /CC_22-23

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN [ "python3" , "-m","unittest","discover","src/docker/test"]

CMD [ "python3" , "-m","unittest","discover","src/docker/test"]

FROM python:3.5
MAINTAINER Maksim Kislenko <m.kislenko@corp.mail.ru>

RUN apt-get update

WORKDIR /opt/loader
COPY ./src ./
COPY ./deploy ./

RUN pip install -r requirements.txt
RUN chmod 777 ./start.sh

EXPOSE 80
CMD ["./start.sh"]

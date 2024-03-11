FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ACCEPT_EULA=Y
WORKDIR /code

RUN apt-get update -y \
    && apt-get install -y

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql18 mssql-tools

RUN apt-get update && apt-get install -y unixodbc-dev 

RUN apt-get install -y freetds-dev freetds-bin
RUN apt-get install -y iputils-ping
# RUN apt install sudo
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
# RUN sudo apt remove libodbc2
# RUN sudo apt install libodbc2
EXPOSE 4370

COPY . /code/

# docker stack deploy -c docker-compose.yml qualabels-stack
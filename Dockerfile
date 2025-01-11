FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ACCEPT_EULA=Y
WORKDIR /code

RUN apt-get update -y \
    && apt-get install -y

# RUN apt-get install -y sudo
# RUN sudo sysctl -w vm.overcommit_memory=1

RUN apt-get update -y && apt-get install -y apt-utils
RUN apt-get update -y && apt-get install -y iputils-ping
# RUN apt install sudo

RUN apt-get update \
    && apt-get install -y curl apt-transport-https gnupg2 unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 mssql-tools 

ENV PATH="$PATH:/opt/mssql-tools/bin"

RUN apt-get update \
    && apt-get install -y \
    gnupg2 \
    curl \
    && apt-get update \
    && apt-get install -y \
    freetds-dev \
    freetds-bin \
    freetds-common \
    libct4 \
    tdsodbc \
    unixodbc \
    unixodbc-dev 

RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
# RUN sudo apt remove libodbc2
# RUN sudo apt install libodbc2
EXPOSE 4370

COPY . /code/

# docker stack deploy -c docker-compose.yml qualabels-stack
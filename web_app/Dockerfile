FROM python:3.11.9
LABEL authors="ove"


ENV django=web_app
RUN echo Рабочий каталог Django ./${django}


COPY ./${django}/requirements.txt /temp/requirements.txt

COPY ./${django} /${django}
WORKDIR /${django}
EXPOSE 8000

# Без libpq5 не работает psycopg3.
# apt отсутствует в alpine версии
RUN apt install libpq5

RUN pip install -r /temp/requirements.txt

# Без этой строчки команда Django manage.py collectstatic выдаёт Permission error
RUN chmod a+rwx -R /${django}

RUN chmod +x /${django}/run_app.sh

# Запускаемся от имени ove почему-то
RUN adduser --disabled-password ove
USER ove

ENTRYPOINT ["/web_app/run_app.sh"]


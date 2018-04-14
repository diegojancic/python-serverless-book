FROM python:3.6-alpine

COPY requirements.txt /

EXPOSE 80

RUN pip install virtualenv \
    && virtualenv /var/venv \
    && source /var/venv/bin/activate \
    && pip install -r requirements.txt

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

CMD ["/var/venv/bin/python", "/code/manage.py", "runserver", "0.0.0.0:80"]
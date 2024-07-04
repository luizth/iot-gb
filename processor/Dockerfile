FROM python:3.9

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY . /code
WORKDIR /code
CMD python3 app.py

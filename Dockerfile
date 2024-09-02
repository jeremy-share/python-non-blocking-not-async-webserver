FROM python:3.11

RUN     pip install --upgrade pip

RUN     mkdir -p /opt/project
WORKDIR /opt/project

COPY requirements.in .
RUN pip install -r requirements.in

CMD python3 src/main.py

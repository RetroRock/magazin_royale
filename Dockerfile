FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

USER 9000

CMD [ "server.py"]

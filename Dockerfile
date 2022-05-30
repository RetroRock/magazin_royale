# Alpine is missing dependencies
# FROM python:3.8-alpine
FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# Permission errors
# RUN useradd -ms /bin/bash magazin_royale

COPY . /app

WORKDIR /app

# Permission errors
# RUN chown -R magazin_royale:magazin_royale /app
# 
# RUN chmod 750 /app
# 
# USER magazin_royale

ENTRYPOINT [ "python" ]

CMD [ "src/server.py"]
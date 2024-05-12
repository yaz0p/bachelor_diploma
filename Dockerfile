FROM python:3.12.3-bullseye

WORKDIR /app

COPY . .

RUN pip install -r req.txt

RUN apt-get update && apt-get install -y nano
RUN apt-get update && apt-get install -y wget bzip2 libxtst6 libgtk-3-0\
 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev

CMD ["/bin/bash", "-c", "python main.py"]

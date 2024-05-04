FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y wget cron

# ========================
# การใช้งาน selenium นั้น จำเป็นต้องมี Web browser ติดตั้งอยู่บนเครื่อง
# สองคำสั่งนี้ คือ การสั่งให้ Download และ install Google Chrome ที่เป็น Stable Version ล่าสุด

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# ========================

WORKDIR /lumpini_cronjob

ADD . /lumpini_cronjob

COPY crontab /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

RUN pip install pipenv
RUN pipenv install --ignore-pipfile --system

CMD ["cron", "-f"]
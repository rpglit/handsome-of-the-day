FROM python:3.12-alpine
RUN apk add py3-pip
RUN apk add --update py3-pip
RUN apk add git
RUN pip3 install psycopg2-binary
RUN git clone https://github.com/rpglit/handsome-of-the-day.git
WORKDIR /handsome-of-the-day/Bot
RUN mkdir logs
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python3 -u main.py >> ./logs/bot.log 2>&1"]

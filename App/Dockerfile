FROM python:3-alpine

WORKDIR /usr/src/app

ADD requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 3000

COPY . .

CMD ["python3", "-u", "App.py"]

FROM python:3-alpine

ADD requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 3000

ADD App.py .

CMD ["python3", "App.py"]

FROM python:3-alpine

ADD requirements.txt .

RUN pip3 install -r requirements.txt

ADD App.py .

CMD ["python3", "App.py"]

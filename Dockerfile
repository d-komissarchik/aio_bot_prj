FROM python:alpine
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot
COPY . /usr/src/bot
RUN pip install -r requirements.txt
CMD ["python", "app.py"]



FROM python:3
WORKDIR /jkchess-rest-api
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install Flask flask-cors nltk requests uwsgi
ADD . /jkchess-rest-api
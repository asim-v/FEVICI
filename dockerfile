# 1 
FROM python:3.6

# 2
RUN pip install werkzeug==0.16.0
RUN pip install Flask gunicorn sqlalchemy flask_session psycopg2
# 3
COPY / /app
WORKDIR /app

# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
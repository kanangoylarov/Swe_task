
FROM python:3.12.3-slim


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["gunicorn", "--bind", "0.0.0.0:443", "wsgi:app"]

EXPOSE 443

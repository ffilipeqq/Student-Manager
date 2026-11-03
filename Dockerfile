FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r -requirements,txt

COPY . .

RUN mkdir -p instance/log instance/exports

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt requirements-container.txt ./

RUN python -m pip install --no-cache-dir -r requirements-container.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
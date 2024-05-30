FROM python:3.11-slim

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD python main.py

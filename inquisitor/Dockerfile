FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y gcc python3-dev

COPY inquisitor.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN chmod +x inquisitor.py

CMD ["python3", "inquisitor.py"]
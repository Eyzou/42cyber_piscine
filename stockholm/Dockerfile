FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y gcc python3-dev libssl-dev

WORKDIR /infection
COPY stockholm.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python stockholm.py; tail -f /dev/null"]
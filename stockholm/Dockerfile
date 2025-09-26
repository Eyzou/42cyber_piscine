FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y gcc python3-dev libssl-dev \
    apt-get install -y openssl

WORKDIR /infection
COPY stockholm.py .
COPY requirements.txt .
COPY /other/salut.c .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "tail -f /dev/null"]
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y gcc python3-dev libssl-dev && \
    apt-get install -y openssl

WORKDIR /app

COPY stockholm.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN chmod +x stockholm.py

RUN mkdir -p /root/infection && \
    echo "This is a test document" > /root/infection/test.txt && \
    echo "PDF test content" > /root/infection/document.pdf && \
    echo "Image test data" > /root/infection/photo.jpg && \
    echo "Excel test data" > /root/infection/data.xlsx && \
    echo "Word test content" > /root/infection/report.docx && \
    echo "Presentation data" > /root/infection/slides.pptx

CMD ["sh", "-c", "tail -f /dev/null"]
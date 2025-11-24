FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/passwords_etl

RUN dbt parse

ENV DAGSTER_HOME=/app/tmp_dagster_home
RUN mkdir -p $DAGSTER_HOME

EXPOSE 3000

WORKDIR /app/orchestration

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        unzip \
    && rm -rf /var/lib/apt/lists/*

RUN update-ca-certificates

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_DIR=/etc/ssl/certs \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

CMD ["dagster", "dev", "--host", "0.0.0.0", "--port", "3000"]

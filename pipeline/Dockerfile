FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pipeline/requirements.txt .

RUN pip install -r requirements.txt

COPY ./flow /app/flow

COPY ./migrations /app/migrations

COPY pipeline/pipeline-crontab /etc/cron.d/pipeline-crontab

COPY pipeline/entrypoint.sh /app/entrypoint.sh

RUN chmod 700 /app/entrypoint.sh

RUN chmod 0644 /etc/cron.d/pipeline-crontab

RUN crontab /etc/cron.d/pipeline-crontab

RUN touch /var/log/cron.log

CMD [ "/app/entrypoint.sh" ]
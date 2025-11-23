FROM python:3.12-slim

# ---------------------------
# 1. Base working directory
# ---------------------------
WORKDIR /app

# Avoid interactive tzdata installs etc.
ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------
# 2. Install python deps
# ---------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------
# 3. Copy project
# ---------------------------
COPY . .

# ---------------------------
# 5. Prepare dbt
# ---------------------------
WORKDIR /app/passwords_etl

# dbt parse must run WITH correct working directory
RUN dbt parse

# ---------------------------
# 6. Dagster home
# ---------------------------
ENV DAGSTER_HOME=/app/tmp_dagster_home
RUN mkdir -p $DAGSTER_HOME

# ---------------------------
# 7. Expose port
# ---------------------------
EXPOSE 3000

# ---------------------------
# 8. Runtime directory
# ---------------------------
WORKDIR /app/orchestration

# ---------------------------
# 9. Launch dagster dev
# ---------------------------
CMD ["dagster", "dev", "--host", "0.0.0.0", "--port", "3000"]

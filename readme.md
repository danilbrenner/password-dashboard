# Password dashboard

```shell

docker compose exec orchestration sh -c "
export STORAGE_CONNECTION_STRING=\"<AZURE BLOB STORAGE CONNECTION STRING>\"
cd ../passwords_etl
dbt run-operation init_db


```
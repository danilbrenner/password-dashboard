{% macro init_db() %}
{% set conn_str = env_var('STORAGE_CONNECTION_STRING') %}
{% set sql %}
INSTALL azure;
LOAD azure;
CREATE OR REPLACE PERSISTENT SECRET azure_passwords (
            TYPE azure,
            CONNECTION_STRING '{{ conn_str }}',
            SCOPE 'azure://password-dashboard/'
        );
{% endset %}
{% do run_query(sql) %}
{% endmacro %}

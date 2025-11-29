FROM grafana/grafana:12.3-ubuntu

USER root

# Install curl, gzip, unzip and certificates
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gzip unzip ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# fall back to the common grafana uid/gid (472) if user/group not present in base image
# Ensure plugins directory exists and set ownership (be robust if grafana user/group isn't present)
RUN mkdir -p /var/lib/grafana/plugins \
    && if id -u grafana >/dev/null 2>&1; then \
         chown -R "$(id -u grafana):$(id -g grafana)" /var/lib/grafana /var/log/grafana /etc/grafana; \
       else \
         chown -R 472:472 /var/lib/grafana /var/log/grafana /etc/grafana; \
       fi

# Download MotherDuck DuckDB datasource plugin from GitHub (pinned release) and extract it into plugins
# If the download fails at build time the build will continue but print a warning.
RUN set -eux; \
    PLUGIN_URL="https://github.com/motherduckdb/grafana-duckdb-datasource/releases/download/v0.4.0/motherduck-duckdb-datasource-0.4.0.zip"; \
    TMP_ZIP="/tmp/motherduck.zip"; \
    if curl -fSL "$PLUGIN_URL" -o "$TMP_ZIP"; then \
        unzip -o "$TMP_ZIP" -d /var/lib/grafana/plugins/; \
        chown -R grafana:grafana /var/lib/grafana/plugins/ 2>/dev/null || chown -R 472:472 /var/lib/grafana/plugins/; \
        rm -f "$TMP_ZIP"; \
    else \
        echo "Warning: failed to download MotherDuck plugin from $PLUGIN_URL"; \
    fi

USER grafana

ENV GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=motherduck-duckdb-datasource \
  GF_AUTH_ANONYMOUS_ENABLED=true \
  GF_AUTH_ANONYMOUS_ORG_ROLE=Admin \
  GF_AUTH_DISABLE_LOGIN_FORM=true \
  GF_AUTH_DISABLE_SIGNOUT_MENU=true

EXPOSE 3000

# Keep base image entrypoint/cmd

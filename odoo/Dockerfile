FROM odoo:9

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python-ldap \
    && rm -rf /var/lib/apt/lists/*

USER odoo
FROM odoo:9

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python-ldap \
    && rm -rf /var/lib/apt/lists/*

#Passage du blog en mode authentifié, pour interdire l'accès public:
RUN sed -i 's/auth="public"/auth="user"/g' /usr/lib/python2.7/dist-packages/openerp/addons/website_blog/controllers/main.py

USER odoo

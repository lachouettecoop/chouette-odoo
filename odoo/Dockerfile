FROM odoo:9

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python-ldap \
    && rm -rf /var/lib/apt/lists/*

# Passage en mode authentification obligatoire en remplacant
#    auth="public" par auth="user"
# Le premier et le dernier sed doit s'appliquer qu'à la méthode web_login que le module
# website a redéfinis comme étant "public" au lieu de "none" dans le module web hérité
# et on ne veut pas passer web_login à auth="user" sinon => boucle de redirection infinie !
RUN sed -i -e 's/@http.route(website=True, auth="public")/@http.route(website=True, auth="none")/' \
        /usr/lib/python2.7/dist-packages/openerp/addons/website/controllers/main.py \
    && sed -i -e 's/auth=['"'"'"]public['"'"'"]/auth="user"/g' \
        /usr/lib/python2.7/dist-packages/openerp/addons/web*/controllers/main.py \
    && sed -i -e 's/@http.route(website=True, auth="none")/@http.route(website=True, auth="public")/' \
        /usr/lib/python2.7/dist-packages/openerp/addons/website/controllers/main.py

USER odoo

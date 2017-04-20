FROM odoo:9

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python-ldap \
        python-simplejson \
    && rm -rf /var/lib/apt/lists/*

ENV ADDONS=/usr/lib/python2.7/dist-packages/openerp/addons

# Fix pour un bug lors de la mise à jour de Odoo 9.0-20160324 à Odoo 9.0-20170207
# et de l'éxécution de la commande de mise à jour de la base:
#     openerp-server -d db -u all
# on obtient l'exception:
#     File "/usr/lib/python2.7/dist-packages/openerp/fields.py", line 628, in _add_trigger
#         field = model._fields[name]
#     KeyError: 'is_portal'
# La clé 'is_portal' définie par le module 'portal', n'est pas trouvée dans le champ
# 'website.menu.group_ids' , défini dans le module 'website'
# Solution trouvée: faire en sorte que le module 'website' dépende du module 'portal':
RUN sed -i -e "s/'depends': \[/'depends': \['portal', /" \
        $ADDONS/website/__openerp__.py

# Dans la vue web "Calendrier":
# - activation par défaut de "Calendriers de tout le monde"
# - début plage horaire à 8h
RUN sed -i -e 's/is_checked: false/is_checked: true/' \
        $ADDONS/calendar/static/src/js/base_calendar.js \
    && sed -i -e 's/firstHour: 6,/firstHour: 8,/' \
        $ADDONS/web_calendar/static/lib/fullcalendar/js/fullcalendar.js


## Passage en mode authentification obligatoire en remplacant
##    auth="public" par auth="user"
## Le premier et le dernier sed doit s'appliquer qu'à la méthode web_login que le module
## website a redéfinis comme étant "public" au lieu de "none" dans le module web hérité
## et on ne veut pas passer web_login à auth="user" sinon => boucle de redirection infinie !
#RUN sed -i -e 's/@http.route(website=True, auth="public")/@http.route(website=True, auth="none")/' \
#        $ADDONS/website/controllers/main.py \
#    && sed -i -e 's/auth=['"'"'"]public['"'"'"]/auth="user"/g' \
#        $ADDONS/web*/controllers/main.py \
#    && sed -i -e 's/@http.route(website=True, auth="none")/@http.route(website=True, auth="public")/' \
#        $ADDONS/website/controllers/main.py

USER odoo

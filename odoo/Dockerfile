FROM odoo:9

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python-simplejson \
        python-ldap \
        python-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt

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

USER odoo

FROM odoo:10

USER root

COPY ./source.list /etc/apt/sources.list
COPY ./pgpd.list /etc/apt/sources.list.d/pgdg.list
COPY ./apt-config /etc/apt/apt.conf.d/99force-archive
COPY ./addons/OpenUpgrade/requirements.txt /root/requirements.txt

RUN apt-get update
# RUN apt-cache policy pip >> aa.txt
# RUN apt-cache madison pip >> aa.txt

# RUN apt-get install -y --force-yes libc6
RUN pip install --upgrade pip==10.0.1
RUN pip install --upgrade pip
RUN apt-get install -y --force-yes libpq5=11.16-0+deb10u1 libpq-dev=11.16-0+deb10u1 libtiff5-dev
RUN apt-get install -y --force-yes libxml2 libxml2-dev libxslt1-dev python-dev gcc
RUN apt-get install -y --force-yes zlib1g-dev libsasl2-dev libldap2-dev libssl-dev

# odoo:9
RUN apt-get install -y --force-yes libtiff5-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
RUN pip install pysftp

# RUN cd /mnt/extra-addons/OpenUpgrade && pip install -r requirements.txt  --ignore-installed

RUN pip install openupgradelib

RUN cd /root && pip install -r requirements.txt  --ignore-installed

# ENV PATH="${PATH}:/usr/bin"
# RUN echo "odoo:x:105:109::/var/lib/odoo:/bin/false" >> /etc/passwd

# RUN mv /usr/bin/odoo_bak /usr/bin/odoo


USER odoo

# ENTRYPOINT ["/entrypoint.sh"]

# CMD ["odoo"]
#!/bin/bash

cd `dirname $0` || exit -1

case $1 in
    "")
        docker-compose up -d
        ;;
    init)
        test -e docker-compose.yml || cp docker-compose.yml.dist docker-compose.yml
        test -e data/odoo/etc/openerp-server.conf || cp data/odoo/etc/openerp-server.conf.dist data/odoo/etc/openerp-server.conf
        docker-compose run -u root odoo bash -c 'chown -R odoo:odoo /etc/odoo/*; chmod -R 777 /var/lib/odoo'
        ;;
    bash)
        ODOO_CONTAINER=`docker-compose ps |grep _odoo_ |cut -d" " -f1`
        docker exec -it $ODOO_CONTAINER $*
        ;;
    psql)
        POSTGRES_USER=`grep POSTGRES_USER docker-compose.yml|cut -d= -f2`
        POSTGRES_PASS=`grep POSTGRES_PASS docker-compose.yml|cut -d= -f2`
        DB_CONTAINER=`docker-compose ps |grep _db_ |cut -d" " -f1`
        docker exec -it $DB_CONTAINER env PGPASSWORD="$POSTGRES_PASS2" psql db $POSTGRES_USER
        ;;
    build|config|create|down|events|exec|kill|logs|pause|port|ps|pull|restart|rm|run|start|stop|unpause|up)
        docker-compose $*
        ;;
    *)
        cat <<HELP
Utilisation : $0 [COMMANDE]
  init         : initialise
               : lance les conteneurs
  bash         : lance bash sur le conteneur odoo
  psql         : lance psql sur le conteneur db, en mode interactif
  stop         : stoppe les conteneurs
  rm           : efface les conteneurs
  logs         : affiche les logs des conteneurs
HELP
        ;;
esac


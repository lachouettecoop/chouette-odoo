#!/bin/bash

set -e
cd `dirname $0`

function container_full_name() {
    # workaround for docker-compose ps: https://github.com/docker/compose/issues/1513
    echo `docker inspect -f '{{if .State.Running}}{{.Name}}{{end}}' \
            $(docker-compose ps -q) | cut -d/ -f2 | grep $1`
}

case $1 in
    "")
        docker-compose up -d
        ;;
    init)
        test -e docker-compose.yml || cp docker-compose.yml.dist docker-compose.yml
        test -e data/odoo/etc/openerp-server.conf \
            || cp data/odoo/etc/openerp-server.conf.dist data/odoo/etc/openerp-server.conf
        docker-compose run --rm db chown -R postgres:postgres /var/lib/postgresql
        docker-compose run --rm -u root odoo bash -c \
            "chown -R odoo:odoo /etc/odoo/*.conf; chmod -R 777 /var/lib/odoo"
        ;;
    upgrade)
        read -rp "Êtes-vous sûr de vouloir effacer et mettre à jour les images et conteneurs Docker ? (o/n) "
        if [[ $REPLY =~ ^[oO]$ ]] ; then
            old_release=`docker-compose run --rm odoo env|grep ODOO_RELEASE`
            docker-compose pull
            docker-compose build
            docker-compose stop
            docker-compose rm -f
            new_release=`docker-compose run --rm odoo env|grep ODOO_RELEASE`
            if [ "$new_release" != "$old_release" ] ; then
                echo "***********************************************n"
                echo "* NOUVELLE VERSION ODOO : $new_release"
                echo "* IL FAUT METTRE À JOUR SA BASE DE DONNEE"
                echo "***********************************************"
                $0 update
            else
                $0
            fi
        fi
        ;;
    update)
        echo "Mise à jour de la base Odoo, voire https://doc.odoo.com/install/linux/updating/"
        echo "Une fois la mise a jour terminée, arretez Odoo (^C) et relancer le normalement"
        echo "L'opération est longue, vérifiez avec la commande 'top' qu'elle est bien terminée"
        read -rp "Êtes-vous sûr ? (o/n) "
        if [[ $REPLY =~ ^[oO]$ ]] ; then
            docker-compose stop odoo
            $0 init
            docker-compose run --rm odoo openerp-server -d db -u all
        fi
        ;;
    debug)
        docker-compose stop odoo
        docker-compose run --rm odoo openerp-server \
            --load=base,web,website \
            --logfile=/dev/stdout --log-level=debug
        ;;
    bash)
        ODOO_CONTAINER=`container_full_name _odoo_`
        docker exec -it $ODOO_CONTAINER $*
        ;;
    psql)
        POSTGRES_USER=`grep POSTGRES_USER docker-compose.yml|cut -d= -f2`
        POSTGRES_PASS=`grep POSTGRES_PASS docker-compose.yml|cut -d= -f2`
        DB_CONTAINER=`container_full_name _db_`
        docker exec -it $DB_CONTAINER env PGPASSWORD="$POSTGRES_PASS2" psql db $POSTGRES_USER
        ;;
    build|config|create|down|events|exec|kill|logs|pause|port|ps|pull|restart|rm|run|start|stop|unpause|up)
        docker-compose $*
        ;;
    *)
        cat <<HELP
Utilisation : $0 [COMMANDE]
  init         : initialise les données
               : lance les conteneurs
  upgrade      : met à jour les images et les conteneurs Docker
  update       : met à jour la base Odoo suite à un changement de version mineure
  bash         : lance bash sur le conteneur odoo
  psql         : lance psql sur le conteneur db, en mode interactif
  stop         : stoppe les conteneurs
  rm           : efface les conteneurs
  logs         : affiche les logs des conteneurs
HELP
        ;;
esac


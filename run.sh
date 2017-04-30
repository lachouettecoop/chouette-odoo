#!/bin/bash

set -e
cd `dirname $0`

function container_full_name() {
    # workaround for docker-compose ps: https://github.com/docker/compose/issues/1513
    echo `docker inspect -f '{{if .State.Running}}{{.Name}}{{end}}' \
            $(docker-compose ps -q) | cut -d/ -f2 | grep -E "_${1}_[0-9]"`
}

function dc_dockerfiles_images() {
    DOCKERDIRS=`grep -E '^\s*build:' docker-compose.yml|cut -d: -f2 |xargs`
    for dockerdir in $DOCKERDIRS; do
        echo `grep "^FROM " ${dockerdir}/Dockerfile |cut -d' ' -f2|xargs`
    done
}


function dc_exec_or_run() {
    CONTAINER_SHORT_NAME=$1
    CONTAINER_FULL_NAME=`container_full_name ${CONTAINER_SHORT_NAME}`
    shift
    if test -n "$CONTAINER_FULL_NAME" ; then
        # container already started
        docker exec -it $CONTAINER_FULL_NAME $*
    else
        # container not started
        docker-compose run --rm $CONTAINER_SHORT_NAME $*
    fi
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
            for image in `dc_dockerfiles_images`; do
                docker pull $image
            done
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
        echo "Une fois la mise a jour terminée, relancer Odoo normalement"
        read -rp "Êtes-vous sûr ? (o/n) "
        if [[ $REPLY =~ ^[oO]$ ]] ; then
            docker-compose stop odoo
            $0 init
            docker-compose run --rm odoo openerp-server -d db -u all --stop-after-init
        fi
        ;;
    prune)
        read -rp "Êtes-vous sûr de vouloir effacer les conteneurs et images Docker innutilisés ? (o/n)"
        if [[ $REPLY =~ ^[oO]$ ]] ; then
            # Note: la commande docker system prune n'est pas dispo sur les VPS OVH
            # http://stackoverflow.com/questions/32723111/how-to-remove-old-and-unused-docker-images/32723285
            exited_containers=$(docker ps -qa --no-trunc --filter "status=exited")
            test "$exited_containers" != ""  && docker rm $exited_containers
            dangling_images=$(docker images --filter "dangling=true" -q --no-trunc)
            test "$dangling_images" != "" && docker rmi $dangling_images
        fi
        ;;
    debug)
        docker-compose stop odoo
        shift
        docker-compose run --rm odoo openerp-server \
            --logfile=/dev/stdout --log-level=debug \
            --debug --dev \
            $*
        ;;
    bash)
        dc_exec_or_run odoo $*
        ;;
    shell)
        shift
        dc_exec_or_run odoo odoo.py shell -d db $*
        ;;
    psql|pg_dump|psqlrestore)
        case $1 in
            psql)        cmd=psql;         option="-it";;
            pg_dump)     cmd="pg_dump -c"; option=     ;;
            psqlrestore) cmd=psql;         option="-i" ;;
        esac
        POSTGRES_USER=`grep POSTGRES_USER docker-compose.yml|cut -d= -f2`
        POSTGRES_PASS=`grep POSTGRES_PASS docker-compose.yml|cut -d= -f2|xargs`
        DB_CONTAINER=`container_full_name db`
        shift
        if [ $# == 0 ] ; then set -- db ; fi # default database = db
        docker exec $option $DB_CONTAINER env PGPASSWORD="$POSTGRES_PASS" PGUSER=$POSTGRES_USER $cmd $*
        ;;
    listmodules)
        shift
        if [ $# == 0 ] ; then set -- db ; fi # default database = db
        echo "SELECT name FROM ir_module_module WHERE state='installed' ORDER BY name;" | $0 psqlrestore -A -t $*
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
  prune        : efface les conteneurs et images Docker inutilisés
  debug        : lance Odoo en mode debug
  bash         : lance bash sur le conteneur odoo
  shell        : lance Odoo shell (python)
  psql         : lance psql sur le conteneur db, en mode interactif
  pg_dump      : lance pg_dump sur le conteneur db
  psqlrestore  : permet de rediriger un dump vers la commande psql
  listmodules  : list installed modules
  stop         : stoppe les conteneurs
  rm           : efface les conteneurs
  logs         : affiche les logs des conteneurs
HELP
        ;;
esac


#!/bin/bash

set -e
cd `dirname $0`

function container_full_name() {
    # Retourne le nom complet du coneneur $1 si il est en cours d'exécution
    # workaround for docker-compose ps: https://github.com/docker/compose/issues/1513
    ids=$(docker-compose ps -q)
    if [ "$ids" != "" ] ; then
        echo `docker inspect -f '{{if .State.Running}}{{.Name}}{{end}}' $ids \
              | cut -d/ -f2 | grep -E "_${1}_[0-9]"`
    fi
}

function dc_dockerfiles_images() {
    # Retourne la liste d'images Docker depuis les Dockerfile build listés dans docker-compose.yml
    local DOCKERDIRS=`grep -E '^\s*build:' docker-compose.yml|cut -d: -f2 |xargs`
    local dockerdir
    for dockerdir in $DOCKERDIRS; do
        echo `grep "^FROM " ${dockerdir}/Dockerfile |cut -d' ' -f2|xargs`
    done
}

function dc_exec_or_run() {
    # Lance la commande $2 dans le container $1, avec 'exec' ou 'run' selon si le conteneur est déjà lancé ou non
    local CONTAINER_SHORT_NAME=$1
    local CONTAINER_FULL_NAME=`container_full_name ${CONTAINER_SHORT_NAME}`
    shift
    if test -n "$CONTAINER_FULL_NAME" ; then
        # container already started
        docker exec -it $CONTAINER_FULL_NAME $*
    else
        # container not started
        docker-compose run --rm $CONTAINER_SHORT_NAME $*
    fi
}

function select_database() {
    # Enregistre le nom de la base de données a utiliser dans la variable 'database'
    readarray -t database < <( $0 listdb )
    if [ ${#database[@]} -gt 1 ] ; then
        echo "Quellle base de données utiliser?" > /dev/stderr
        local i
        for i in "${!database[@]}"; do
            echo " $i : ${database[$i]}" > /dev/stderr
        done
        local index
        read -n 1 -r -p '?' index > /dev/stderr
        echo > /dev/stderr
        if [ "$index" -ge 0 -a "$index" -lt ${#database[@]} ]; then
            database="${database[$index]}"
        else
            exit -1;
        fi
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
            old_release=`dc_exec_or_run odoo env|grep ODOO_RELEASE`
            echo "ODOO_RELEASE= $old_release"
            docker-compose pull
            for image in `dc_dockerfiles_images`; do
                docker pull $image
            done
            docker-compose build
            docker-compose stop
            docker-compose rm -f
            new_release=`dc_exec_or_run odoo env|grep ODOO_RELEASE`
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
        echo "Mise à jour des bases Odoo, voire https://doc.odoo.com/install/linux/updating/"
        read -rp "Êtes-vous sûr ? (o/n) "
        if [[ $REPLY =~ ^[oO]$ ]] ; then
            function backup_and_update () {
                database=$1
                backupfile="pg_dump-$database-`date '+%Y-%m-%dT%H:%M:%S'`.gz"
                echo "Sauvegarde avant mise à jour de la base $1 dans $backupfile"
                $0 pg_dump $database |gzip > $backupfile
                docker-compose run --rm odoo openerp-server -u all --stop-after-init -d $database
            }
            $0 init
            docker-compose stop odoo
            shift
            if [ $# == 0 ] ; then
                for database in `$0 listdb` ; do
                    backup_and_update $database
                done
            else
                backup_and_update $1
            fi
        fi
        $0
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
        if [ $# == 0 ] ; then select_database; set -- $database ; fi
        dc_exec_or_run odoo odoo.py shell -d $*
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
        if [ "$DB_CONTAINER" = "" ] ; then 
            echo "Démare le conteneur db" > /dev/stderr
            docker-compose up -d db > /dev/stderr
            sleep 3
            DB_CONTAINER=`container_full_name db`
        fi
        shift
        if [ $# == 0 ] ; then select_database; set -- $database ; fi
        docker exec $option $DB_CONTAINER env PGPASSWORD="$POSTGRES_PASS" PGUSER=$POSTGRES_USER $cmd $*
        ;;
    listdb)
        echo "SELECT datname FROM pg_database WHERE datistemplate=false AND NOT datname in ('postgres','odoo');" | $0 psqlrestore -A -t postgres
        ;;
    listmod)
        shift
        if [ $# == 0 ] ; then select_database; set -- $database ; fi
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
  listdb       : liste les bases de données
  listmod      : liste les modules Odoo installés
  stop         : stope les conteneurs
  rm           : efface les conteneurs
  logs         : affiche les logs des conteneurs
HELP
        ;;
esac


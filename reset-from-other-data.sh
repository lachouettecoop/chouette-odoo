#!/bin/bash

DATA_TO_USE=$1

set -e

DATA_TO_USE=$1
VIRTUAL_HOST=`grep VIRTUAL_HOST docker-compose.yml|cut -d= -f2`

echo "Démarrage de la remise à zéro de cette instance d'Odoo."
echo "... les données seront resynchronisées depuis " $DATA_TO_USE

if [ -z "$DATA_TO_USE" ] ; then
    echo "ERREUR: chemin source non fourni"
    exit -1
fi

if [ "$VIRTUAL_HOST" == "espace-membres.lachouettecoop.fr" ] ; then
    echo "ERREUR: remplacement des données de 'espace-membres.lachouettecoop.fr' interdit"
    exit -1
fi

read -rp "Êtes-vous sûr ? (o/n)"
if [[ ! ( $REPLY =~ ^[oO]$ ) ]] ; then
    exit 0
fi


echo "Arrêt et suppression de l'instance actuelle"
docker-compose stop && docker-compose rm -vf

echo "Suppression des données actuelles"
rm -rf ./data

echo "Récupération des données distantes"
rsync -avzL $DATA_TO_USE .

echo "Redémarrage de la base de donnée avec les données à jour"
docker-compose up -d db

if [ "$VIRTUAL_HOST" != "espace-membres.lachouettecoop.fr" ] ; then
    echo "Désactivation des serveurs de mail autre que Mailcatcher"
    sleep 2 # attente que la base de donnée soit lancée
    ./run.sh psqlrestore << EOSQL
UPDATE ir_mail_server SET active=false WHERE name NOT LIKE '%Mailcatcher%';
EOSQL
fi

echo "Redémarrage d'Odoo"
docker-compose up -d


echo "... et voilà !"

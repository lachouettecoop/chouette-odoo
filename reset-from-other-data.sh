#!/bin/bash

DATA_TO_USE=$1

set -e

DATA_TO_USE=$1
VIRTUAL_HOST=`grep VIRTUAL_HOST docker-compose.yml|cut -d= -f2`

echo "Démarrage de la remise à zéro de cette instance d'Odoo."
echo "... les données seront resynchronisées depuis " $DATA_TO_USE

if [[ "$DATA_TO_USE" != */data ]] ; then
    echo "ERREUR: le chemin source ne se termine pas par */data"
    exit -1
fi

if [[ ("$VIRTUAL_HOST" == "espace-membres.lachouettecoop.fr") || ("$VIRTUAL_HOST" == "sas.lachouettecoop.fr") ]] ; then
    echo "ERREUR: remplacement des données de 'espace-membres.lachouettecoop.fr ou sas.***' interdit"
    exit -1
fi

read -rp "Êtes-vous sûr ? (o/n)"
if [[ ! ( $REPLY =~ ^[oO]$ ) ]] ; then
    exit 0
fi


echo "Arrêt et suppression de l'instance actuelle"
docker-compose stop && docker-compose rm -vf

#echo "Suppression des données actuelles"
#rm -rf ./data

echo "Récupération des données distantes"
rsync -avzL --checksum --delete $DATA_TO_USE .

echo "Redémarrage de la base de donnée avec les données à jour"
docker-compose up -d db

if [[ ("$VIRTUAL_HOST" != "espace-membres.lachouettecoop.fr") && ("$VIRTUAL_HOST" != "sas.lachouettecoop.fr") ]] ; then
    echo "Désactivation des serveurs de mail autre que Mailcatcher:"
    sleep 4 # attente que la base de donnée soit lancée
    ./run.sh psql << SQL1
UPDATE ir_mail_server SET active=false WHERE name NOT LIKE '%Mailcatcher%';
SQL1
    echo "Activation des comptes de tests ADMIN,Compta,EDIT,Vente,Lambda:"
    ./run.sh psql << SQL2
UPDATE res_users SET active=true where login='Chouette_ADMIN@lachouettecoop.fr';
UPDATE res_users SET active=true where login='Chouette_compta@lachouettecoop.fr';
UPDATE res_users SET active=true where login='chouettevente1@lachouettecoop.fr';
UPDATE res_users SET active=true where login='chouettevente2@lachouettecoop.fr';
UPDATE res_users SET active=true where login='chouettevente3@lachouettecoop.fr';
UPDATE res_users SET active=true where login='utilisateurlambda@lachouettecoop.fr';
SQL2
fi

echo "Redémarrage d'Odoo"
docker-compose up -d


echo "... et voilà !"

#!/bin/bash

DATA_TO_USE=$1

echo "Démarrage de la remise à zéro de cette instance d'Odoo."
echo "... les données seront resynchronisées depuis " $DATA_TO_USE

echo "TODO Ajouter ici une confirmation car ça craint si exécuté par erreur, en expliquant les conséquences tout ça"
echo "ou même faire en sorte que si le VIRTUAL_HOST du docker-compose ne contient ni preprod ou test on bloque"

echo "Arrêt et suppression de l'instance actuelle"
docker-compose stop && docker-compose rm -vf

echo "Suppression des données actuelles"
rm -rf ./data

echo "Récupération des données distantes"
rsync -avzL $DATA_TO_USE .

echo "Redémarrage de l'instance avec les données à jour"
docker-compose up -d

echo "... et voilà !"

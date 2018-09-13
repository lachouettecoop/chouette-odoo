# La Chouette Coop - Odoo

Ce projet contient l'outil de gestion de "[La chouette coop](http://lachouettecoop.fr/)". N'hésitez pas à installer une version en locale sur votre poste ou votre serveur. 


## Contexte
* l'installation est décrite pour une distribution Debian
* les conteneurs docker sont placés dans le répertoire Dev qui est à la racine du compte utilisateur

## Pré-requis

* Créer un répertoire ou mettre les conteneurs
```
mkdir ~/Dev
cd Dev
```

* récupérer le projet
```
git clone --recursive https://github.com/lachouettecoop/chouette-odoo/
```

* avoir [Docker](http://docs.docker.com/)
```
cd ~/Dev
wget https://get.docker.com/ -O script.sh
chmod +x script.sh; ./script.sh
```

* avoir [Docker Compose](http://docs.docker.com/compose/install/)
```
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

* quitter la session et la réouvrir pour pouvoir bénéficier des modifications de droits associés aux groupes

* tester l'installation de docker-compose
```
docker-compose --version
```


## Récupérer les données depuis un site en production, par exemple

* Récupérer la base de données : se connecter sur le site `https://monsite/web/database/manager` puis faire un "backup"


## Installer nginx-proxy

* récupérer [nginx-proxy](https://github.com/jwilder/nginx-proxy)
```
cd ~/Dev
git clone --recursive https://github.com/jwilder/nginx-proxy/
```

* éditer le fichier docker-compose.yml `vi ~/dev/chouette-info/docker-compose.yml` et changer la valeur de la variable "VIRTUAL_HOST" à "odoo.lachouettecoop.test"

* lier odoo.lachouettecoop.test à 127.0.0.1 : éditer /etc/hosts et ajouter la ligne "127.0.0.1	odoo.lachouettecoop.test"

* Il faut un long timeout configuré pour nginx-proxy sinon des problèmes pourraient survenir à l'installation d'extensions. Exemple :

```
proxy_connect_timeout 600;
proxy_send_timeout 600;
proxy_read_timeout 600;
send_timeout 600;
```


* lancer nginx-proxy
```
cd ~/Dev/ngix-proxy
docker-compose start
```

## Utilisation

Pour lancer l'application exécutez simplement les commandes : 

```
cd ~Dev/chouette-odoo
./run.sh init
./run.sh
```

## Après installation

* lancer odoo : `https://odoo.lachouettecoop.test`
* restaurer le backup de la base Odoo (cf étape précédente) : se connecter `https://monsite/web/database/manager` puis faire un "restore"
* Activer le mode "dev" dans l'admin odoo
* Supprimer l'envoi des mails (config smtp)

## Relancer

Dans l'ordre :
* se placer dans le répertoire ngix-proxy et `docker-compose start`
* se placer dans le répertoire chouette-odoo et `docker-compose start`
* depuis un navigateur lancer odoo : odoo.lachouettecoop.test


## Licence

[GPL v2.0](LICENSE)

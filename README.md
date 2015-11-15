# La Chouette Coop - Odoo

Ce projet contient l'outil de gestion de "[La chouette coop](http://lachouettecoop.fr/)".

*Pour rejoindre l'aventure au sein du groupe informatique contactez moi ou
utilisez le site !*

## Pré-requis

* récupérer le projet (`git clone`)
* avoir [Docker](http://docs.docker.com/) et [Docker Compose](http://docs.docker.com/compose/install/) installé

## Utilisation

Pour lancer l'application exécutez simplement la commande :

```
docker-compose up -d
```

### Bonus

Si vous avez [nginx-proxy](https://github.com/jwilder/nginx-proxy) en place (suivre procédure de lancement très simple sur la doc) le site sera accessible à l'url : http://odoo.lachouettecoop.test/

Il vous faudra un long timeout configuré pour nginx-proxy sinon des problèmes pourraient survenir à l'installation d'extensions. Exemple :

```
proxy_connect_timeout 600;
proxy_send_timeout 600;
proxy_read_timeout 600;
send_timeout 600;
```

## Licence

[GPL v2.0](LICENSE)
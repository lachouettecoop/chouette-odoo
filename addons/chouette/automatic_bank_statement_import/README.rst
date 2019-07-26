.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3


=============================================
Le Filament - Automatic Bank Statement Import
=============================================

Ce module permet d'importer automatiquement des relevés bancaires au format OFX de manière quotidienne
Ce module suppose que les relevés sont disponibles sur le serveur (par défaut dans /ofx/bank_account_import.ofx)
Pour générer ces relevés OFX, weboob et son module boobank en particulier peuvent être utilisés sur le serveur dans un cron quotidien (à implémenter en dehors d'Odoo - non couvert par ce module)
Ce module modifie aussi l'affichage par défaut sur le tableau de bord de facturation pour les banques, en affichant le montant des Lettrages, des Mouvements (si différent des Lettrages), la date et le montant du dernier relevé.

Credits
=======

Contributors ------------

* Remi Cazenave <remi@le-filament.com>


Maintainer ----------

.. image:: https://le-filament.com/img/logo-lefilament.png
   :alt: Le Filament
   :target: https://le-filament.com

This module is maintained by Le Filament

// Modify behaviour of addons/web/static/src/js/widgets/user_menu.js
openerp.user_menu_chouette = function(instance, local) {
     instance.web.UserMenu.include({
          on_menu_support_chouette: function () {
              window.open('https://gestion.lachouettecoop.fr/projects/assistance/issues/new', '_blank');
          },
     });
}

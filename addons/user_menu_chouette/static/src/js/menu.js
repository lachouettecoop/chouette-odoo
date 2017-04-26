odoo.define('user_menu_chouette.support_chouette', function (require) {
"use strict";

var Model = require('web.Model');
var UserMenu = require('web.UserMenu');

// Modify behaviour of addons/web/static/src/js/widgets/user_menu.js
UserMenu.include({
    on_menu_support_chouette: function () {
        //window.open('https://gestion.lachouettecoop.fr/projects/assistance/issues/new', '_blank');
        var P = new Model('ir.config_parameter');
        P.call('get_param', ['x_user_menu_support_url']).then(function(url) {
            window.open(url);
        });
    }
});

});

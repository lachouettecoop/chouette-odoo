odoo.define('user_menu_chouette.support_chouette', function (require) {
"use strict";

var Model = require('web.Model');
var UserMenu = require('web.UserMenu');

var support_link = "";
setTimeout(function() {
    new Model('ir.config_parameter')
        .call('get_param', ['x_user_menu_support_url'])
        .then(function(url) { support_link=url; });
}, 3000);

// Modify behaviour of addons/web/static/src/js/widgets/user_menu.js
UserMenu.include({
    on_menu_support_chouette: function () {
        window.open(support_link, '_blank');
    }
});

});

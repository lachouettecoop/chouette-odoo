# -*- coding: utf-8 -*-
##############################################################################
#
#    eCommerce deactivation
#    Copyright La Chouette Coop
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp.addons.website_sale.controllers.main as main

class website_sale_deactivation(main.website_sale):
    """Override website_sale methods
       that where defining an @http.route,
       here we don't define @http.route to deactivate it.
    """
    def pricelist_change(self, *params, **params_dict):
        pass
    def shop(self, *params, **params_dict):
        pass
    def product(self, *params, **params_dict):
        pass
    def pricelist(self, *params, **params_dict):
        pass
    def cart(self, *params, **params_dict):
        pass
    def cart_update(self, *params, **params_dict):
        pass
    def cart_update_json(self, *params, **params_dict):
        pass
    def checkout(self, *params, **params_dict):
        pass
    def confirm_order(self, *params, **params_dict):
        pass
    def extra_info(self, *params, **params_dict):
        pass
    def payment(self, *params, **params_dict):
        pass
    def payment_transaction(self, *params, **params_dict):
        pass
    def payment_get_status(self, *params, **params_dict):
        pass
    def payment_validate(self, *params, **params_dict):
        pass
    def payment_confirmation(self, *params, **params_dict):
        pass
    def print_saleorder(self, *params, **params_dict):
        pass
    def add_product(self, *params, **params_dict):
        pass
    def change_styles(self, *params, **params_dict):
        pass
    def change_sequence(self, *params, **params_dict):
        pass
    def change_size(self, *params, **params_dict):
        pass
    def tracking_cart(self, *params, **params_dict):
        pass
    def get_unit_price(self, *params, **params_dict):
        pass


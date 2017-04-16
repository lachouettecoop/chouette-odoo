# -*- coding: utf-8 -*-
##############################################################################
#
#    No public HTTP authentification, Odoo addon
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

import openerp
from openerp.osv import orm
from openerp.addons.web.http import request


class ir_http(orm.AbstractModel):
    _inherit = 'ir.http'
    def _auth_method_public(self):
        """Redefine "public" auth method to call "user" auth method
           except for /, /web/login and their needed content (image,css,js)
        """
        path = request.httprequest.path
        public = False
        if path in ("/","/longpolling/poll","/web/login","/web/image/51472", "/web/image/59179"):
            public = True
        elif path.startswith("/web/content/"):
            path = path[13:].split("/")
            public = (len(path) == 2) and path[-1] in ("website.assets_frontend.0.css", "website.assets_frontend.js", "web.assets_common.0.css", "web.assets_common.js")
        if public:
            if not request.session.uid:
                website = self.pool['website'].get_current_website(request.cr, openerp.SUPERUSER_ID, context=request.context)
                if website:
                    request.uid = website.user_id.id
                else:
                    request.uid = self.pool['ir.model.data'].xmlid_to_res_id(request.cr, openerp.SUPERUSER_ID, 'base', 'public_user')
            else:
                request.uid = request.session.uid
        else:
            self._auth_method_user()


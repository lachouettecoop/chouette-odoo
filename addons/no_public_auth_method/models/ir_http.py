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
import openerp.addons.website.models.ir_http
from openerp.osv import orm
from openerp.addons.web.http import request


PUBLIC_PATH=(
    "/",
    "/web/login",
    "/web/image/51472",
    "/web/image/59179",
    "/longpolling/poll",
)

PUBLIC_WEB_CONTENT=(
    "web.assets_common.js",
    "web.assets_common.0.css",
    "website.assets_frontend.js",
    "website.assets_frontend.0.css",
)

class ir_http(orm.AbstractModel):
    _inherit = 'ir.http'
    def _auth_method_public(self):
        """Redefine "public" auth method to call "user" auth method
           except for PUBLIC_PATH and PUBLIC_WEB_CONTENT for which
           we call website "public" auth method.
        """
        path = request.httprequest.path
        if path.startswith("/web/content/"):
            content_path = path[13:].split("/")
            keep_public = (len(content_path) == 2) and (content_path[1] in PUBLIC_WEB_CONTENT)
        else:
            keep_public = path in PUBLIC_PATH
        if keep_public:
            openerp.addons.website.models.ir_http.ir_http._auth_method_public(self)
        else:
            self._auth_method_user()


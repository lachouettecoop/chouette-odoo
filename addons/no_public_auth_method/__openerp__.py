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
{
    'name' : 'No public HTTP authentification',
    'description' : ('Replace "public" authentification by "user", except for / and /web/login'
                     'REM: "none" autheftification, like for /database/manager is still possible'),
    'version' : '0.1',
    'depends' : ['base', 'website'],
    'category' : 'Extra Tools',
    'data' : [],
    'installable': True,
}

# This file is part of ldap_chouette.  ldap_chouette is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright La Chouette Coop

{
    'name' : 'La Chouette Coop LDAP authentication',
    'description' : ('Override native Odoo LDAP authentication with La '
                     'Chouette Coop specific LDAP schema'),
    'version' : '0.1',
    'depends' : ['base'],
    #'description': < auto-loaded from README file
    'category' : 'Extra Tools',
    'data' : [
    ],
    'auto_install': False,
    'installable': True,
    'external_dependencies' : {
        'python' : ['ldap'],
    }
}

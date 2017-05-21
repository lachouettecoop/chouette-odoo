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

import logging

from openerp.osv import osv


_logger = logging.getLogger(__name__)


class ChouetteLDAP(osv.osv):
    _inherit = 'res.company.ldap'

    def map_ldap_attributes(self, cr, uid, conf, login, ldap_entry):
        """
        Compose values for a new resource of model res_users,
        based upon the retrieved ldap entry and the LDAP settings.

        :param dict conf: LDAP configuration
        :param login: the new user's login
        :param tuple ldap_entry: single LDAP result (dn, attrs)
        :return: parameters for a new resource of model res_users
        :rtype: dict
        """
        name = '{0} {1}'.format(ldap_entry[1]['description'][0],
                                ldap_entry[1]['sn'][0])

        barcode = ldap_entry[1]['homeDirectory'][0]

        _logger.info('Authenticating {0}'.format(ldap_entry[1]['cn'][0]))
        values = { 'name': name, 'login': login, 'email': login, 'barcode': barcode, 'company_id': conf['company']
                   }
        return values

ChouetteLDAP()  # call the class (required)

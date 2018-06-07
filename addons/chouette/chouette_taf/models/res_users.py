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
import requests
import urllib2
import ssl
import json
import os

from openerp.osv import osv
from openerp import api

_logger = logging.getLogger(__name__)


class UsersTaf(osv.osv):
    _inherit = 'res.users'
    
    @api.one
    def get_taf_attributes(self):
        """
        Gets TAF information from Google scriptsx
        """
	

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = os.environ['URL_TAF'] + self.email
        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx))
        request = urllib2.Request(url)
        try:
            result = opener.open(request)
            return json.loads(result.read())
        except urllib2.URLError as e:
            return e.reason


# -*- coding: utf-8 -*-
##############################################################################
#
#    Mail server force domain
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
#from openerp.addons.base.ir.ir_mail_server import ir_mail_server
from openerp.models import AbstractModel
from email.utils import parseaddr


def email_address_domain(email_address):
    email_address = parseaddr(email_address)[1] # Remove textual name
    if "@" in email_address:
        return email_address.split("@")[1]
    else:
        return None

class ir_mail_server(AbstractModel):
    _inherit = 'ir.mail_server'
    def build_email(self, email_from, email_to, subject, body, email_cc=None, email_bcc=None, reply_to=False,
            attachments=None, message_id=None, references=None, object_id=False, subtype='plain', headers=None,
            body_alternative=None, subtype_alternative='plain'):
        """Redifine build_email to force sender address domain (email_from)
           to match configuration value 'mail.catchall.domain'.
        """

        allowed_domain = self.env['ir.config_parameter'].sudo().get_param('mail.catchall.domain')

        if allowed_domain and email_address_domain(email_from) != allowed_domain:
            if not reply_to:
                reply_to = email_from
                email_from = self._get_default_bounce_addr()
            elif email_address_domain(reply_to) == allowed_domain:
                subject = subject + " (" + email_from + ")"
                email_from = reply_to
                reply_to = None
            else:
                subject = subject + " (" + email_from + ")"
                email_from = self._get_default_bounce_addr()

        return super(ir_mail_server, self).build_email(
            email_from, email_to, subject, body, email_cc, email_bcc, reply_to,
            attachments, message_id, references, object_id, subtype, headers,
            body_alternative, subtype_alternative)


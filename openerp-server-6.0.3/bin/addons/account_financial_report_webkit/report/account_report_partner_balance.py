# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright Camptocamp SA 2011
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


from report import report_sxw
from tools.translate import _
import pooler
from datetime import datetime

from partner_balance_header_webkit import CommonPartnerBalanceReportHeaderWebkit
from webkit_parser_header_fix import HeaderFooterTextWebKitParser


class PartnerBalanceWebkit(report_sxw.rml_parse, CommonPartnerBalanceReportHeaderWebkit):

    def __init__(self, cursor, uid, name, context):
        super(PartnerBalanceWebkit, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr
        
        company = self.pool.get('res.users').browse(self.cr, uid, uid, context=context).company_id
        header_report_name = ' - '.join((_('PARTNER BALANCE'), company.name, company.currency_id.name))

        footer_date_time = self.formatLang(str(datetime.today()), date_time=True)

        self.localcontext.update({
            'cr': cursor,
            'uid': uid,
            'report_name': _('Partner Balance'),
            'display_account': self._get_display_account,
            'display_account_raw': self._get_display_account_raw,
            'filter_form': self._get_filter,
            'target_move': self._get_target_move,
            'display_target_move': self._get_display_target_move,
            'display_partner_account': self._get_display_partner_account,
            'accounts': self._get_accounts_br,
            'additional_args': [
                ('--header-font-name', 'Helvetica'),
                ('--footer-font-name', 'Helvetica'),
                ('--header-font-size', '10'),
                ('--footer-font-size', '6'),
                ('--header-left', header_report_name),
                ('--header-spacing', '2'),
                ('--footer-left', footer_date_time),
                ('--footer-right', ' '.join((_('Page'), '[page]', _('of'), '[topage]'))),
                ('--footer-line',),
            ],
        })

    def _get_initial_balance_mode(self, start_period):
        """ Force computing of initial balance for the partner balance,
        because we cannot use the entries generated by
        OpenERP in the opening period.

        OpenERP allows to reconcile move lines between different partners,
        so the generated entries in the opening period are wrong.
        """
        return 'initial_balance'

    def set_context(self, objects, data, ids, report_type=None):
        """Populate a ledger_lines attribute on each browse record that will be used
        by mako template"""
        objects, new_ids, context_report_values = self.compute_partner_balance_data(data)

        self.localcontext.update(context_report_values)
        return super(PartnerBalanceWebkit, self).set_context(objects, data, new_ids,
                                                            report_type=report_type)

HeaderFooterTextWebKitParser('report.account.account_report_partner_balance_webkit',
                             'account.account',
                             'addons/account_financial_report_webkit/report/templates/account_report_partner_balance.mako',
                             parser=PartnerBalanceWebkit)

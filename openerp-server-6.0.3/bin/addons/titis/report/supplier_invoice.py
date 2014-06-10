# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from datetime import time, date, datetime
from report import report_sxw
from tools.translate import _
from tools import amount_to_text_en

class supplier_invoice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(supplier_invoice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'convert': self.convert,
        })

        self.context = context

    def convert(self, amount):
        amt_en = amount_to_text_en.amount_to_text(amount, 'en', 'Dolar')
        return amt_en

report_sxw.report_sxw(
    'report.supplier_invoice',
    'account.invoice',
    'addons/titis/report/supplier_invoice.rml',
    parser=supplier_invoice, header=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

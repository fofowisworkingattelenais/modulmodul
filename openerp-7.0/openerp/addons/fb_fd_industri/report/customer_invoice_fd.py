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

import time
from openerp.report import report_sxw

class customer_invoice_fd(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(customer_invoice_fd, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_product_desc': self.get_product_desc,
            'get_product_code': self.get_product_code,

        })

    def get_product_desc(self, invoice_line):
        desc = invoice_line.product_id.name
        return desc

    def get_product_code(self, invoice_line):
        desc = invoice_line.product_id.default_code
        return desc



report_sxw.report_sxw(
    'report.customer.invoice.fd',
    'account.invoice',
    'addons/fb_fd_industri/report/customer_invoice_fd.rml',
    parser=customer_invoice_fd,
    header= False
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

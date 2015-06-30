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

    def get_product_desc(self, move_line):
        i = 0
        nama= []

        self.cr.execute("   select b.product_name as product_name\
                                from product_product a \
                                    left join tat_product_customerinfo b \
                                        on a.id = b.product_id \
                            where a.id = %s \
        " % move_line.product_id.id)

        cat = self.cr.dictfetchall()
        if i < len(cat):
            for ii in cat:
                product_name = ii['product_name']
                if not product_name:
                    return move_line.product_id.name
                return product_name

    def get_product_code(self, move_line):
        i = 0
        self.cr.execute("   select b.product_code as product_code\
                                from product_product a \
                                    left join tat_product_customerinfo b \
                                        on a.id = b.product_id \
                            where a.id = %s \
        " % move_line.product_id.id)

        cat = self.cr.dictfetchall()
        if i < len(cat):
            for ii in cat:
                product_code = ii['product_code']
                if not product_code:
                    return move_line.product_id.code
                return product_code




report_sxw.report_sxw(
    'report.customer.invoice.fd',
    'account.invoice',
    'addons/fb_fd_industri/report/customer_invoice_fd.rml',
    parser=customer_invoice_fd,
    header= False
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

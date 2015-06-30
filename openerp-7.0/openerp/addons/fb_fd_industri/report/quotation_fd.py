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
from openerp.osv import osv
from openerp import pooler

class quotation_fd(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(quotation_fd, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'user': self.pool.get('res.users').browse(cr, uid, uid, context),
            'get_product_desc': self.get_product_desc,
            'get_product_code': self.get_product_code,
            'get_min_quantity': self.get_min_quantity,
            'show_discount':self._show_discount
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

    def get_min_quantity(self, move_line):
        i = 0
        self.cr.execute("   select b.min_qty as moq\
                                from product_product a \
                                    left join tat_product_customerinfo b \
                                        on a.id = b.product_id \
                            where a.id = %s \
        " % move_line.product_id.id)

        cat = self.cr.dictfetchall()
        if i < len(cat):
            for ii in cat:


                moq = ii['moq']

                return moq


    def _show_discount(self, uid, context=None):
        cr = self.cr
        try:
            group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'group_discount_per_so_line')[1]
        except:
            return False
        return group_id in [x.id for x in self.pool.get('res.users').browse(cr, uid, uid, context=context).groups_id]


report_sxw.report_sxw('report.quotation.fd','sale.order','addons/fb_fd_industri/report/quotation_fd.rml',parser=quotation_fd, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:






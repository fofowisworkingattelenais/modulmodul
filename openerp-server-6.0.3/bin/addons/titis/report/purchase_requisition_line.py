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

from dateutil import parser
import xml
import copy
from operator import itemgetter
import time
import datetime
import re
from report import report_sxw

class purchase_requisition_line(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(purchase_requisition_line, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'isi_laporan': self.lines,
        })
        self.context = context



    def lines(self, form):

        res = {}
        query = {}
        i = 0
        self.cr.execute("select \
                            a.name AS requisition_id, \
                            a.date_start AS date_start, \
                            a.pcs_by AS pcs_by, \
                            a.product_qty AS product_qty, \
                            c.name  AS product_uom_id, \
                            d.name_template AS product_id, \
                            e.name AS order_id, \
                            a.po_date_order AS po_date_order, \
                            a.po_date_order - a.date_start AS delivery\
                        from \
                            purchase_requisition_line a\
                            left join purchase_requisition b \
                                on a.requisition_id = b.id \
                            left join product_uom c \
                                on a.product_uom_id = c.id \
                            left join product_product d \
                                on a.product_id = d.id \
                            left join purchase_order e \
                                on a.order_id = e.id \
                        where (a.date_start BETWEEN %s AND %s) \
                        order by a.date_start \
                    ", (form['date_start'], form['date_end']))
        query = self.cr.dictfetchall()

        if i < len(query):
            while i < len(query):
                if query[i]['po_date_order'] is False:
                    query[i]['po_date_order'] = ''
                res = {
                    'requisition_id': query[i]['requisition_id'] or '-',
                    'date_start': query[i]['date_start'] or '',
                    'product_qty': query[i]['product_qty'] or '',
                    'pcs_by': query[i]['pcs_by'] or '',
                    'product_uom_id': query[i]['product_uom_id'] or '',
                    'product_id': query[i]['product_id'] or '',
                    'order_id': query[i]['order_id'] or '',
                    'po_date_order': query[i]['po_date_order'] or '',
                    'delivery': query[i]['delivery'] or '',
                    'date_from': form['date_start'],
                    'date_to': form['date_end']
                }


                self.isi_laporan.append(res)
                i += 1

        return self.isi_laporan


        # ctx = self.context.copy()
        # ctx['date_from'] = form['date_start']
        # ctx['date_to'] = form['date_end']

        # ids = self.pool.get('purchase.requisition.line').search(self.cr, self.uid, ctx)
        # for i in self.pool.get('purchase.requisition.line').browse(self.cr, self.uid, ids):
        #     print i
        #     print 'waku'
            # res = {
            #     'requisition_id': i.requisition_id,
            #     'date_start': i.date_start,
            #     'pcs_by': i.pcs_by,
            #     'product_qty': i.product_qty,
            #     'product_uom_id': i.product_uom_id,
            #     'product_id': i.product_id,
            #     'order_id': i.order_id,
            #     'po_order_date': i.po_order_date,
            #     # 'periode_start_date': ctx['date_from'],
            #     # 'periode_end_date': ctx['date_to']
            # }
            # self.isi_laporan.append(res)
        # print self.isi_laporan
        # return self.isi_laporan

report_sxw.report_sxw('report.purchase_requisition_line', 'purchase.requisition.line', 'addons/titis/report/purchase_requisition_line.rml', parser=purchase_requisition_line, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
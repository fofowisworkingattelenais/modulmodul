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
import locale
from report import report_sxw
import netsvc

class stock_varience_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(stock_varience_report, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.slip_ids = []
        self.localcontext.update({
            'time' : time,
            'locale' : locale,
            'isi_laporan' : self.isi,
            'date_from' : self.get_date_from,
            'date_to' : self.get_date_to,
            'total_amount_price':self.total_amount_price

        })

    def total_amount_price(self):
        # i = 0
        #
        # self.cr.execute("   select distinct SUM(CAST(a.ctn_no as INT)) as total from stock_move a \
        #                         left join stock_picking b on a.picking_id = b.id \
        #                     where a.picking_id = %s \
        # " % move_line.picking_id.id)
        #
        # cat = self.cr.dictfetchall()
        # for ii in cat:
        #     total = ii['total']
        #
        #     return total
        obj_move = self.pool.get('stock.move')
        kriteria = [('picking_id.state','=','done'),('picking_id.date','>=',self.date_from),('picking_id.date','<=',self.date_to)]

        move_ids = obj_move.search(self.cr, self.uid, kriteria)


        if move_ids:
            no = 1
            total = 0
            for move in obj_move.browse(self.cr, self.uid, move_ids):
                total += move.total_cost

            return total

    def isi(self, form):
        l = 0
        obj_move = self.pool.get('stock.move')
        kriteria = [('picking_id.state','=','done'),('picking_id.date','>=',self.date_from),('picking_id.date','<=',self.date_to)]
        move_ids = obj_move.search(self.cr, self.uid, kriteria)
        moves_line = obj_move.browse(self.cr, self.uid, move_ids)
        total_amount_price = self.total_amount_price()
        varience_line = 0
        actual_amount = 0
        actual_cost_price = 0
        if move_ids:
            no = 1
            variance = form['variance'] - total_amount_price
            for move in moves_line:

                varience_line = move.total_cost / total_amount_price * variance
                print varience_line, '+', move.total_cost
                actual_amount = varience_line + move.total_cost
                if actual_amount == 0:
                    actual_cost_price = 0.0
                else:
                    actual_cost_price = actual_amount / move.product_qty

                if move.type == 'in':
                   move.type = 'Getting Goods'
                elif move.type == 'out':
                    move.type = 'Sending Goods'
                elif move.type == 'internal':
                    move.type = 'Internal'
                print no
                res =   {
                            'no' : no,
                            'description' : move.name,
                            'references' : move.picking_id.name,
                            'source' : move.origin,
                            'shipping_type' : move.type,
                            'product' : move.product_id.name,
                            'kuantitas' : move.product_qty,
                            'satuan' : move.product_uom.name,
                            'standard_cost_price': move.cost_price,
                            'total_cost' : move.total_cost,
                            'var': varience_line,
                            'actual_amount':actual_amount,
                            'actual_cost_price':actual_cost_price,
                            'serial_number': move.prodlot_id.name,
                            'pack' : '',
                            'location_id' : move.location_id.name,
                            'location_dest_id' : move.location_dest_id.name,
                            'date' : move.date[8:10] + '-' + move.date[5:7] + '-' + move.date[0:4],
                            'date_expected' : move.date_expected[8:10] + '-' +move.date_expected[5:7] + '-' + move.date_expected[0:4],
                            'status' : move.state,
                }
                no += 1

                self.isi_laporan.append(res)

        return self.isi_laporan



    def get_date_from(self):

        return '%s/%s/%s' % (self.date_from[8:10], self.date_from[5:7], self.date_from[0:4])

    def get_date_to(self):

        return '%s/%s/%s' % (self.date_to[8:10], self.date_to[5:7], self.date_to[0:4])




    def set_context(self, objects, data, ids, report_type=None):
        self.date_from = data['form']['date_from']
        self.date_to = data['form']['date_to']


        return super(stock_varience_report, self).set_context(objects, data, ids, report_type=report_type)

report_sxw.report_sxw('report.fb_mtm.stock_variance', 'stock.move', 'addons/fb_mtm/report/stock_varience_report.rml', parser=stock_varience_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


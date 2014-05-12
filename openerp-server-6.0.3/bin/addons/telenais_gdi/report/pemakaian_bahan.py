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
from report import report_sxw
from osv import osv
import pooler
import locale

class pemakaian_bahan(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(pemakaian_bahan, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'locale' : locale,
            'total_jumlah' : self.total_jumlah,
        })
        
    def total_jumlah(self, move_line):
        total = 0.0
        for move in move_line:
            total += move.product_qty
            
        return total


report_sxw.report_sxw('report.gdi.pemakaian_bahan','stock.picking','addons/telenais_gdi/report/pemakaian_bahan.rml',parser=pemakaian_bahan)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

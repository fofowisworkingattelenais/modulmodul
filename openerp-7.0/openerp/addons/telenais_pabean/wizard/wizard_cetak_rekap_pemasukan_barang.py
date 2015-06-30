# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from osv import fields, osv
from osv.orm import browse_record, browse_null
from tools.translate import _


class wizard_cetak_rekap_pemasukan_barang(osv.osv_memory):
    _name = 'gdi.wizard_cetak_rekap_pemasukan_barang'
    _description = 'Wizard Cetak Rekapitulasi Pemasukan Barang'

    _columns = {
                'date_from': fields.date(string='Date From', required=True),
                'date_to': fields.date(string='Date To', required=True),
                # 'location_id': fields.many2one(obj='stock.location', string='Location', required='True'),
                # 'location_id': fields.char('Location', size=64, select=True, readonly=True),
    }

    def cetak_laporan(self, cr, uid, ids, context=None):
        datas = {}
        if context is None:
            context = {}

        data = self.read(cr, uid, ids, [], context)[0]

        datas = {
            'ids': context.get('active_ids', []),
            'model': 'stock.move',
            'form': data
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'gdi.rekap_penerimaan_barang',
            'datas': datas
        }


wizard_cetak_rekap_pemasukan_barang()



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

class rekap_penerimaan_barang(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(rekap_penerimaan_barang, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.slip_ids = []
        self.localcontext.update({
            'time' : time,
            'locale' : locale,
            'isi_laporan' : self.isi,
            'date_from' : self.get_date_from,
            'date_to' : self.get_date_to,
        })
        
    def isi(self):
        obj_move = self.pool.get('stock.move')
        kriteria = [('picking_id.type','=','in'),('picking_id.state','=','done'),('picking_id.date','>=',self.date_from),('picking_id.date','<=',self.date_to),('picking_id.chk_import','=',True)]
        
        move_ids = obj_move.search(self.cr, self.uid, kriteria)
        
        if move_ids:
            no = 1
            for move in obj_move.browse(self.cr, self.uid, move_ids):
                res =   {
                            'no' : no,
                            'jenis_dokumen' : move.picking_id.jenis_dokumen_id.name,
                            'nomor_dokumen' : move.picking_id.nomor_dokumen_pabean,
                            'tanggal_dokumen' : move.picking_id.tanggal_dokumen_pabean,
                            'nomor_bast' : move.picking_id.name,
                            'tanggal_bast' : '%s/%s/%s' % (move.picking_id.date[8:10],move.picking_id.date[5:7], move.picking_id.date[0:4]),
                            'pemasok' : move.picking_id.address_id and move.picking_id.address_id.partner_id.name or '-',
                            'kode_barang' : move.product_id.default_code,
                            'nama_barang' : move.product_id.name,
                            'satuan' : move.product_uom.name,
                            'kuantitas' : move.product_qty,
                            'nilai_barang' : move.price_unit * move.product_qty,
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
        

        return super(rekap_penerimaan_barang, self).set_context(objects, data, ids, report_type=report_type)           

report_sxw.report_sxw('report.gdi.rekap_penerimaan_barang', 'stock.move', 'addons/telenais_gdi/report/rekap_penerimaan_barang.rml', parser=rekap_penerimaan_barang, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


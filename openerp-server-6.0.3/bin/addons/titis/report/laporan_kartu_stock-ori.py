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

from datetime import time, date, datetime
from report import report_sxw

class laporan_kartu_stock(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(laporan_kartu_stock, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,  
            'isi_laporan' : self.lines,
            'nama_uom' : self.get_nama_uom,
            'nama_product' : self.get_nama_product,
            'default_code' : self.get_default_code,
            'category_name' : self.get_category_name,
            'location_name' : self.get_location_name,
            'date_from' : self.get_date_from,
            'date_to' : self.get_date_to,
        })
        self.context = context
        
    def get_tanggal(self, tanggal):
        month = tanggal[5:7]
        nama_bulan = ''
        tanggal_cnvt = ''
        
        bulan = {
                '01' : 'Januai',
                '02' : 'Pebruari',
                '03' : 'Maret',
                '04' : 'April',
                '05' : 'Mei',
                '06' : 'Juni',
                '07' : 'Juli',
                '08' : 'Agustus',
                '09' : 'September',
                '10' : 'Oktober',
                '11' : 'November',
                '12' : 'Desember'
                }

        nama_bulan = bulan.get(month, False)
        if not nama_bulan:
            return '-'
        
        tanggal_cnvt = tanggal[8:10] + ' ' + nama_bulan + ' ' + tanggal[:4]

        return tanggal_cnvt
        
    def get_nama_uom(self, form):
        nama_uom = ''
        obj_product = self.pool.get('product.product')
        
        kriteria = [ ('id','=', form['product_id']) ]
        
        product_ids = obj_product.search(self.cr, self.uid, kriteria)

        for product in obj_product.browse(self.cr, self.uid, product_ids):
            if product:
                nama_uom = product.uom_id.name
                
        return nama_uom
        
    def get_nama_product(self, form):
        nama_product = ''
        obj_product = self.pool.get('product.product')
        
        kriteria = [ ('id','=', form['product_id']) ]
        
        product_ids = obj_product.search(self.cr, self.uid, kriteria)

        for product in obj_product.browse(self.cr, self.uid, product_ids):
            if product:
                nama_product = product.name
                
        return nama_product
        
    def get_default_code(self, form):
        default_code = ''
        obj_product = self.pool.get('product.product')
        
        kriteria = [ ('id','=', form['product_id']) ]
        
        product_ids = obj_product.search(self.cr, self.uid, kriteria)

        for product in obj_product.browse(self.cr, self.uid, product_ids):
            if product:
                default_code = product.default_code
                
        return default_code
        
    def get_category_name(self, form):
        category_name = ''
        obj_product = self.pool.get('product.product')
        
        kriteria = [ ('id','=', form['product_id']) ]
        
        product_ids = obj_product.search(self.cr, self.uid, kriteria)

        for product in obj_product.browse(self.cr, self.uid, product_ids):
            if product:
                category_name = product.categ_id.name
                
        return category_name
        
    def get_location_name(self, form):
        location_name = ''
        obj_stock_location = self.pool.get('stock.location')
        
        kriteria = [ ('id','=', form['location_id']) ]
        
        location_ids = obj_stock_location.search(self.cr, self.uid, kriteria)

        for location in obj_stock_location.browse(self.cr, self.uid, location_ids):
            if location:
                location_name = location.name
                
        return location_name
        
    def lines (self, form):
        res = {}
        query = {}
        i = 0

        self.cr.execute("SELECT A.date, \
                    A.note, \
                    B3.product_qty AS kredit, \
                    B2.product_qty AS debit \
                    FROM stock_move A \
                    LEFT JOIN (SELECT A2.id, \
                    A2.product_qty \
                    FROM stock_move A2 \
                    JOIN stock_location C ON A2.location_dest_id = C.id \
                    WHERE C.id = %s ) B2 ON A.id = B2.id \
                    LEFT JOIN (SELECT A3.id, \
                    A3.product_qty \
                    FROM stock_move A3 \
                    JOIN stock_location C2 ON A3.location_id = C2.id \
                    WHERE C2.id = %s ) B3 ON A.id = B3.id \
                    WHERE product_id = %s \
                    AND A.state = %s \
                    AND (A.location_dest_id = %s OR A.location_id = %s)\
                    ORDER BY A.date " , 
                    (form['location_id'], form['location_id'], form['product_id'], 'done', form['location_id'], form['location_id']))
        query = self.cr.dictfetchall()
        
        if i < len(query):
            while i < len(query):
                
                res = {
                    'tanggal' : self.get_tanggal(query[i]['date']),
                    'masuk' : query[i]['debit'] or '-',
                    'keluar' : query[i]['kredit'] or '-',
                    'stok' : query[i]['debit'] or query[i]['kredit'] or '-',
                    'keterangan' : query[i]['note'],                        
                }           
                self.isi_laporan.append(res)                            
                i+=1

        return self.isi_laporan


    def get_date_from(self):
        
        return '%s/%s/%s' % (self.date_from[8:10], self.date_from[5:7], self.date_from[0:4])
        
    def get_date_to(self):
        
        return '%s/%s/%s' % (self.date_to[8:10], self.date_to[5:7], self.date_to[0:4])


    def set_context(self, objects, data, ids, report_type=None):
        self.date_from = data['form']['date_from']
        self.date_to = data['form']['date_to']
        

        return super(laporan_kartu_stock, self).set_context(objects, data, ids, report_type=report_type)     
        
        
    

report_sxw.report_sxw('report.laporan_kartu_stock', 'stock.move', 'addons/titis/report/laporan_kartu_stock.rml', parser=laporan_kartu_stock, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

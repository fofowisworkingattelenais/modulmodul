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

class saldo_inventory(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(saldo_inventory, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.isi_saldo = []

        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
            'nama_uom' : self.get_nama_uom,
            'nama_product' : self.get_nama_product,
            'default_code' : self.get_default_code,

            'qty_available' : self.get_qty_available,
            'isi_saldo' : self.saldo,
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
        nama_uom = []
        obj_product = self.pool.get('product.product')
        i = 0
        cat = {}
        # categ_id = form['parent_id'][0]

        self.cr.execute(" select distinct(d.product_id) as id from product_template a \
            left join product_category b on a.categ_id = b.parent_left \
            left join product_product c on a.id = c.product_tmpl_id \
            left join stock_move d on c.id = d.product_id \
            where  d.product_id is not null and d.location_id = %s \
        " % form['location_id'][0])

        cat = self.cr.dictfetchall()
        if i < len(cat):
            for ii in cat:

                kriteria = [ ('id','=', ii['id'])]
                product_ids = obj_product.search(self.cr, self.uid, kriteria)

                for product in obj_product.browse(self.cr, self.uid, product_ids):
                    res = {
                        'nama_uom': product.uom_id.name
                    }
                    nama_uom.append(res)
                    i += 1

        return nama_uom

    def get_nama_product(self, form):
        obj_product = self.pool.get('product.product')
        i = 0

        cat = {}
        nama_product = []
        saldo = []

        self.cr.execute(" select \
                                distinct(a.id) as id,\
                                c.default_code as code\
                            from product_template a \
                                 left join product_category b on a.categ_id = b.parent_left \
                                 left join product_product 	c on a.id 	= c.product_tmpl_id \
                                 left join stock_move 	d on c.id 	= d.product_id \
                            where   c.default_code is not null and d.product_id is not null and (d.location_id = %s or d.location_dest_id = %s)\
                            order by   c.default_code asc \
        ", (form['location_id'][0], form['location_id'][0]))

        cat = self.cr.dictfetchall()
        if not cat:
            return {
                        'nama_product': '',
                    }


        if i < len(cat):
            for ii in cat:
                self.cr.execute(" select \
                                    a.standard_price as harga_beli \
                                from product_template a \
                                     left join product_product 	c on a.id 	= c.product_tmpl_id \
                                     left join stock_move 	d on c.id 	= d.product_id \
                                     left join stock_location 	e on d.location_id = e.id \
                                where   c.id = %s \
                                group by a.standard_price\
                                " % ii['id'])

                q = self.cr.dictfetchall()

                for iii in q:
                    results ={
                        'harga_beli': iii['harga_beli'] or '0.0',
                        'location_name': form['location_id'][1],
                    }

                self.cr.execute("   SELECT \
                                        COALESCE(sum(B5.product_qty), 0.000)   masuk_awal,\
                                        COALESCE(sum(B4.product_qty), 0.000)  keluar_awal,\
                                        COALESCE(sum(B2.product_qty), 0.000) masuk,\
                                        COALESCE(sum(B3.product_qty), 0.000) keluar,\
                                        COALESCE(sum(B2.product_qty) - sum(B3.product_qty), 0.000) hasil,\
                                        COALESCE(sum(B5.product_qty)  - sum(B4.product_qty), 0.000) saldo_awal\
                                    FROM stock_move A \
                                        LEFT JOIN (SELECT A2.id,A2.product_qty \
                                            FROM  \
                                                stock_move A2 \
                                                    JOIN stock_location C \
                                                        ON A2.location_dest_id = C.id \
                                            WHERE 	C.id = %s \
                                                    AND (A2.date > %s AND A2.date < %s))\
                                            B2 ON A.id = B2.id \
                                        LEFT JOIN (SELECT A3.id, A3.product_qty \
                                            FROM \
                                                stock_move A3 \
                                                    JOIN stock_location C2 \
                                                        ON A3.location_id = C2.id \
                                            WHERE 	C2.id = %s \
                                                    AND (A3.date > %s AND A3.date < %s) ) \
                                             B3 ON A.id = B3.id \
                                        LEFT JOIN (SELECT A4.id, A4.product_qty \
                                            FROM \
                                                stock_move A4 \
                                                    JOIN stock_location C3 \
                                                        ON A4.location_id = C3.id \
                                            WHERE 	C3.id = %s\
                                                AND (A4.date < %s )  \
                                                AND (A4.location_dest_id = %s OR A4.location_id = %s)) \
                                            B4 ON A.id = B4.id \
                                        LEFT JOIN (SELECT A5.id, A5.product_qty \
                                            FROM \
                                                stock_move A5 \
                                                    JOIN stock_location C4 \
                                                        ON A5.location_dest_id = C4.id \
                                            WHERE 	C4.id = %s \
                                                AND (A5.date < %s ) \
                                                AND (A5.location_dest_id = %s OR A5.location_id = %s)) \
                                            B5 ON A.id = B5.id \
                                    WHERE \
                                        product_id = %s \
                                        AND A.state = %s \
                                        AND (A.location_dest_id = %s OR A.location_id = %s) \
                                    ", (form['location_id'][0], form['date_from'], form['date_to'],
                                        form['location_id'][0], form['date_from'], form['date_to'],
                                        form['location_id'][0], form['date_from'], form['location_id'][0],
                                        form['location_id'][0], form['location_id'][0], form['date_from'],
                                        form['location_id'][0], form['location_id'][0], ii['id'],
                                        'done', form['location_id'][0], form['location_id'][0]))

                query = self.cr.dictfetchall()

                for a in query:

                    if a['masuk_awal'] is None or '':
                        a['masuk_awal'] = 0.000
                    if a['keluar_awal'] is None or '':
                        a['keluar_awal'] = 0.000
                    if a['masuk'] is None or '':
                        a['masuk'] = 0.000
                    if a['keluar'] is None or '':
                        a['keluar'] = 0.000


                    masuk_awal =  a['masuk_awal'] or 0.000
                    keluar_awal = a['keluar_awal'] or 0.000
                    keluar = a['keluar'] or 0.000
                    masuk = a['masuk'] or 0.000
                    hasil =  a['hasil'] or 0.000
                    # saldo_awal = query[i]['masuk_awal']  + query[i]['keluar_awal']
                    # saldo_akhir = (query[i]['masuk_awal'] + query[i]['keluar_awal']) or 0.000 - query[i]['hasil'] or 0.000
                    saldo_awal = (masuk_awal - keluar_awal)  or 0.0
                    saldo_akhir = (saldo_awal + (masuk - keluar)) or 0.0
                    if masuk is None or '' or 0.0:
                        saldo_akhir = saldo_awal - keluar


                    result ={
                        'saldo_akhir':saldo_akhir or '0.0',
                        'pemasukan':masuk or '0.0',
                        'pengeluaran': keluar or '0.0',
                        'saldo_awal': saldo_awal or '0.0',
                        'akhir': saldo_akhir or '0.0',
                        'total_akhir': (masuk - keluar) * iii['harga_beli'] or '0.0'
                    }
                    result.update(results)
                saldo_ak = 0
                kriteria = [ ('id','=', ii['id'])]

                product_ids = obj_product.search(self.cr, self.uid, kriteria)

                for product in obj_product.browse(self.cr, self.uid, product_ids):


                    res = {
                        'nama_product': product.name,
                        'nama_uom': product.uom_id.name,
                        'default_code': product.default_code,
                        'qty_available': product.qty_available,
                        'category_name': product.categ_id.name,
                        'location_name': product.location_id.name,
                        # 'harga_beli': ii['harga_beli'],
                        # 'total': product.qty_available * ii['harga_beli']
                    }
                    res.update(result)
                    nama_product.append(res)
                    saldo_ak += 1
                    i += 1


            return nama_product

    def get_default_code(self, form):
        i = 0
        default_code = ''
        obj_product = self.pool.get('product.product')
        cat = {}

        self.cr.execute(" select distinct(d.product_id) as id from product_template a \
            left join product_category b on a.categ_id = b.parent_left \
            left join product_product c on a.id = c.product_tmpl_id \
            left join stock_move d on c.id = d.product_id \
            where  d.product_id is not null and d.location_id = %s \
        " % form['location_id'][0])

        cat = self.cr.dictfetchall()
        if i < len(cat):
            for ii in cat:

                kriteria = [ ('id','=', ii['id']) ]

                product_ids = obj_product.search(self.cr, self.uid, kriteria)

                for product in obj_product.browse(self.cr, self.uid, product_ids):
                    if product:
                        default_code = product.default_code

        return default_code


    def get_qty_available(self, form):
        qty_available = ''
        obj_product = self.pool.get('product.product')
        i = 0
        cat = {}

        self.cr.execute(" select distinct(d.product_id) as id from product_template a \
            left join product_category b on a.categ_id = b.parent_left \
            left join product_product c on a.id = c.product_tmpl_id \
            left join stock_move d on c.id = d.product_id \
            where  d.product_id is not null and d.location_id = %s \
        " % form['location_id'][0])

        cat = self.cr.dictfetchall()

        if i < len(cat):
            for ii in cat:

                kriteria = [ ('id','=', ii['id']) ]

                product_ids = obj_product.search(self.cr, self.uid, kriteria)

                for product in obj_product.browse(self.cr, self.uid, product_ids):
                    if product:

                        qty_available = product.qty_available



        return qty_available


    def get_category_name(self, form):
        category_name = ''
        obj_product = self.pool.get('product.product')
        i = 0
        cat = {}

        self.cr.execute(" select distinct(d.product_id) as id from product_template a \
            left join product_category b on a.categ_id = b.parent_left \
            left join product_product c on a.id = c.product_tmpl_id \
            left join stock_move d on c.id = d.product_id \
            where  d.product_id is not null and d.location_id = %s \
        " % form['location_id'][0])

        cat = self.cr.dictfetchall()

        if i < len(cat):
            for ii in cat:

                kriteria = [ ('id','=', ii['id']) ]

                product_ids = obj_product.search(self.cr, self.uid, kriteria)

                for product in obj_product.browse(self.cr, self.uid, product_ids):
                    if product:
                        category_name = product.categ_id.name

        return category_name

    def get_location_name(self, form):
        location_name = ''
        obj_stock_location = self.pool.get('stock.location')
        i = 0
        cat = {}
        self.cr.execute(" select distinct(d.product_id) as id from product_template a \
            left join product_category b on a.categ_id = b.parent_left \
            left join product_product c on a.id = c.product_tmpl_id \
            left join stock_move d on c.id = d.product_id \
            where  d.product_id is not null and d.location_id = %s \
        " % form['location_id'][0])

        cat = self.cr.dictfetchall()

        if i < len(cat):
            for ii in cat:

                kriteria = [ ('id','=', ii['id']) ]



                location_ids = obj_stock_location.search(self.cr, self.uid, kriteria)

                for location in obj_stock_location.browse(self.cr, self.uid, location_ids):
                    if location:
                        location_name = location.name

        return location_name

    def saldo(self,form):
        res = {}
        query = {}
        i = 0
        cat = {}
        self.cr.execute(" select distinct(d.product_id) as id from product_template a \
            left join product_category b on a.categ_id = b.parent_left \
            left join product_product c on a.id = c.product_tmpl_id \
            left join stock_move d on c.id = d.product_id \
            where  d.product_id is not null and d.location_id = %s \
        " % form['location_id'][0])

        cat = self.cr.dictfetchall()

        if i < len(cat):
            for ii in cat:


                self.cr.execute("   SELECT \
                                        COALESCE(sum(B5.product_qty), 0.000)   masuk_awal,\
                                        COALESCE(sum(B4.product_qty), 0.000)  keluar_awal,\
                                        COALESCE(sum(B2.product_qty), 0.000) masuk,\
                                        COALESCE(sum(B3.product_qty), 0.000) keluar,\
                                        COALESCE(sum(B2.product_qty) - sum(B3.product_qty), 0.000) hasil,\
                                        COALESCE(sum(B5.product_qty)  - sum(B4.product_qty), 0.000) saldo_awal\
                                    FROM stock_move A \
                                        LEFT JOIN (SELECT A2.id,A2.product_qty \
                                            FROM  \
                                                stock_move A2 \
                                                    JOIN stock_location C \
                                                        ON A2.location_dest_id = C.id \
                                            WHERE 	C.id = %s \
                                                    AND (A2.date > %s AND A2.date < %s))\
                                            B2 ON A.id = B2.id \
                                        LEFT JOIN (SELECT A3.id, A3.product_qty \
                                            FROM \
                                                stock_move A3 \
                                                    JOIN stock_location C2 \
                                                        ON A3.location_id = C2.id \
                                            WHERE 	C2.id = %s \
                                                    AND (A3.date > %s AND A3.date < %s) ) \
                                             B3 ON A.id = B3.id \
                                        LEFT JOIN (SELECT A4.id, A4.product_qty \
                                            FROM \
                                                stock_move A4 \
                                                    JOIN stock_location C3 \
                                                        ON A4.location_id = C3.id \
                                            WHERE 	C3.id = %s\
                                                AND (A4.date < %s )  \
                                                AND (A4.location_dest_id = %s OR A4.location_id = %s)) \
                                            B4 ON A.id = B4.id \
                                        LEFT JOIN (SELECT A5.id, A5.product_qty \
                                            FROM \
                                                stock_move A5 \
                                                    JOIN stock_location C4 \
                                                        ON A5.location_dest_id = C4.id \
                                            WHERE 	C4.id = %s \
                                                AND (A5.date < %s ) \
                                                AND (A5.location_dest_id = %s OR A5.location_id = %s)) \
                                            B5 ON A.id = B5.id \
                                    WHERE \
                                        product_id = %s \
                                        AND A.state = %s \
                                        AND (A.location_dest_id = %s OR A.location_id = %s) \
                                    ", (form['location_id'][0], form['date_from'], form['date_to'],
                                        form['location_id'][0], form['date_from'], form['date_to'],
                                        form['location_id'][0], form['date_from'], form['location_id'][0],
                                        form['location_id'][0], form['location_id'][0], form['date_from'],
                                        form['location_id'][0], form['location_id'][0], ii['id'],
                                        'done', form['location_id'][0], form['location_id'][0]))


                query = self.cr.dictfetchall()
                if i < len(query):
                    if query[i]['masuk_awal'] is None or '':
                        query[i]['masuk_awal'] = 0.000
                    if query[i]['keluar_awal'] is None or '':
                        query[i]['keluar_awal'] = 0.000
                    if query[i]['masuk'] is None or '':
                        query[i]['masuk'] = 0.000
                    if query[i]['keluar'] is None or '':
                        query[i]['keluar'] = 0.000


                    masuk_awal =  query[i]['masuk_awal'] or 0.000
                    keluar_awal = query[i]['keluar_awal'] or 0.000
                    keluar = query[i]['keluar'] or 0.000
                    masuk = query[i]['masuk'] or 0.000
                    hasil =  query[i]['hasil'] or 0.000
                    # saldo_awal = query[i]['masuk_awal']  + query[i]['keluar_awal']
                    # saldo_akhir = (query[i]['masuk_awal'] + query[i]['keluar_awal']) or 0.000 - query[i]['hasil'] or 0.000
                    saldo_awal = (masuk_awal - keluar_awal)  or 0.0
                    saldo_akhir = (saldo_awal + (masuk - keluar)) or 0.0
                    if masuk is None or '' or 0.0:
                        saldo_akhir = saldo_awal - keluar

                    res = {
                        'masuk_awal' :masuk_awal,
                        'keluar_awal' : keluar_awal,
                        'masuk' : masuk,
                        'keluar' : keluar,
                        'saldo_awal': saldo_awal or '0.0',
                        'saldo_akhir': saldo_akhir or '0.0',
                        'date_from': form['date_from'],
                        'date_to': form['date_to']
                    }
                    self.isi_saldo.append(res)
                    i += 1
        return self.isi_saldo


    def lines (self, form):
        res = {}
        query = {}
        i = 0
        cat = {}
        self.cr.execute(" select distinct(d.product_id) as id from product_template a \
            left join product_category b on a.categ_id = b.parent_left \
            left join product_product c on a.id = c.product_tmpl_id \
            left join stock_move d on c.id = d.product_id \
            where  d.product_id is not null and d.location_id = %s \
        " % form['location_id'][0])

        cat = self.cr.dictfetchall()

        if i < len(cat):
            for ii in cat:


                self.cr.execute("   SELECT A.date, \
                            A.note, \
                            B3.product_qty AS kredit, \
                            B2.product_qty AS debit, \
                            P.name AS references, \
                            P.origin AS origin, \
                            R.name AS partner \
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
                            LEFT JOIN stock_picking P \
                            on A.picking_id = P.id \
                            LEFT JOIN res_partner R \
                            on A.partner_id = R.id \
                            WHERE product_id = %s \
                            AND A.state = %s \
                            AND (A.location_dest_id = %s OR A.location_id = %s)\
                            AND (A.date > %s AND A.date < %s)\
                            ORDER BY A.date ",
                                (form['location_id'][0], form['location_id'][0], ii['id'], 'done', form['location_id'][0], form['location_id'][0], form['date_from'], form['date_to']))

                query = self.cr.dictfetchall()
                if i < len(query):
                    while i < len(query):

                        res = {
                            'tanggal' : self.get_tanggal(query[i]['date']),
                            'masuk' : query[i]['debit'] or '-',
                            'keluar' : query[i]['kredit'] or '-',
                            'stok' : query[i]['debit'] or query[i]['kredit'] or '-',
                            'keterangan' : query[i]['note'],
                            'start_date': form['date_from'],
                            'end_date': form['date_to'],
                            'origin': query[i]['origin'],
                            'references': query[i]['references'],
                            'partner': query[i]['partner']
                        }
                        self.isi_laporan.append(res)
                        i += 1

        return self.isi_laporan


    def get_date_from(self):
        return '%s/%s/%s' % (self.date_from[8:10], self.date_from[5:7], self.date_from[0:4])

    def get_date_to(self):
        return '%s/%s/%s' % (self.date_to[8:10], self.date_to[5:7], self.date_to[0:4])


    def set_context(self, objects, data, ids, report_type=None):
        # self.categ_id = data['form']['parent_id'][0]
        self.date_from = data['form']['date_from']
        self.date_to = data['form']['date_to']


        return super(saldo_inventory, self).set_context(objects, data, ids, report_type=report_type)


report_sxw.report_sxw('report.saldo_inventory', 'stock.move', 'addons/fb_stock/report/saldo_inventory.rml', parser=saldo_inventory, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

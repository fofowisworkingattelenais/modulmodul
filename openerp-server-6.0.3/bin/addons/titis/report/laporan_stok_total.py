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

class laporan_stok_total(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(laporan_stok_total, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,  
            'isi_laporan' : self.lines,
            'tanggal' : self.get_tanggal,
        })
        self.context = context
        
    def get_tanggal(self, form):
        tanggal = form['close_date']
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
        
    def lines (self, form):

        return self.isi_laporan

report_sxw.report_sxw('report.laporan_stok_total', 'stock.move', 'addons/titis/report/laporan_stok_total.rml', parser=laporan_stok_total, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

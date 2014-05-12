# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP SA (<http://openerp.com>).
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
from osv import fields, osv
from tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import decimal_precision as dp
import netsvc
from tools.translate import _
from datetime import datetime, date


class wizard_sesuaikan_libur_nasional(osv.osv_memory):
    _name = 'hr.wizard_sesuaikan_libur_nasional'
    _description = 'Wizard Sesuaikan Libur Nasional'

    def default_periode_libur(self, cr, uid, context={}):
        return 'tahun'

    def default_absensi(self, cr, uid, context={}):
        return 'draft'
        
    def default_tahun(self, cr, uid, context={}):
        return date.today().year

    _columns =  {
                'tahun' : fields.integer(string='Tahun', required=True),
                'bulan_id' : fields.many2one(obj='base.bulan', string='Bulan'),
                'periode_libur' : fields.selection(selection=[('bulan','Bulan'),('tahun','Tahun')], string='Periode Liburan', required=True),
                'absensi' : fields.selection(selection=[('confirm','Sudah Dikonfirmasi'),('draft','Belum Dikonfirmasi')], string='Diterapkan Pada Absensi', required=True),
                }
                
    _defaults = {
                'periode_libur' : default_periode_libur,
                'absensi' : default_absensi,
                'tahun' : default_tahun,
                }
                
                
    def jalankan_wizard(self, cr, uid, ids, context={}):
        obj_wizard = self.pool.get('hr.wizard_sesuaikan_libur_nasional')
        obj_history = self.pool.get('hr.contract')   
        obj_bulan = self.pool.get('base.bulan') 
        obj_absensi = self.pool.get('hr.absensi')    
        obj_user = self.pool.get('res.users')
        obj_libur = self.pool.get('hr.libur_nasional')
        obj_timesheet = self.pool.get('hr.timesheet_karyawan')
        
        wizard = obj_wizard.browse(cr, uid, ids)[0]
        
        # ambil user 
        user = obj_user.browse(cr, uid, [uid])[0]
        
        # set tanggal mulai dan tanggal akhir untuk kriteria pencarian data absensi
        if wizard.periode_libur == 'tahun':
            tanggal_mulai = '%s-01-01' % (str(wizard.tahun))
            tanggal_akhir = '%s-12-31' % (str(wizard.tahun))
        else:
            tanggal_mulai = '%s-%s-01' % (str(wizard.tahun), wizard.bulan_id.kode)
            tanggal_akhir = '%s-%s-%s' % (str(wizard.tahun), wizard.bulan_id.kode, str(obj_bulan.jumlah_hari(cr, uid, wizard.bulan_id.id, wizard.tahun))) 
            
        # hari libur
        kriteria_libur = [('tanggal','>=',tanggal_mulai),('tanggal','<=',tanggal_akhir)]       
        libur_ids = obj_libur.search(cr, uid, kriteria_libur)
        tanggal_libur = []
        if libur_ids:
            for libur in obj_libur.browse(cr, uid, libur_ids):
                tanggal_libur.append(libur.tanggal)
        
            
        
        

        #TODO: Kriteria untuk timesheet
        kriteria_timesheet = ['|',('state','=','draft'),('state','=','confirm')]
        timesheet_ids = obj_timesheet.search(cr, uid, kriteria_timesheet)
        
        kriteria = [('tanggal','>=',tanggal_mulai),('tanggal','<=',tanggal_akhir),('tanggal','in',tanggal_libur),('timesheet_id','in',timesheet_ids)]

        # set kriteria status untuk pencarian absensi
        if wizard.absensi == 'draft':
            kriteria.append(('state','=','draft'))
        else:
            kriteria.append(('state','=','confirm'))    
            
        # cari absensi yang memenuhi kriteria
        absensi_ids = obj_absensi.search(cr, uid, kriteria)
        

        # edit absensi menjadi libur
        if absensi_ids:
            val =   {
                    'realisasi_jam_masuk' : False,
                    'realisasi_jam_keluar' : False,
                    'realisasi_mulai_istirahat' : False,
                    'realisasi_selesai_istirahat' : False,
                    'shift_kerja_id' : False,
                    'kode_absen_id' : user.company_id.default_kode_absen_libur_id.id,
                    }
                    
            obj_absensi.write(cr, uid, absensi_ids, val) 
                            
            
        

  
        return {}        
                
wizard_sesuaikan_libur_nasional()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

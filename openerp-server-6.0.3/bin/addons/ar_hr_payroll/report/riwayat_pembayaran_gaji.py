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

class riwayat_pembayaran_gaji(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(riwayat_pembayaran_gaji, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.slip_ids = []
        self.localcontext.update({
            'time' : time,
            'locale' : locale,
            'isi_laporan' : self.isi,
            'slip_ids' : self.slip_ids,
            'nama_karyawan' : self.get_nama_karyawan,
            'nip_karyawan' : self.get_nip_karyawan,
            'tahun_laporan' : self.get_tahun_laporan,
        })
        
    def isi(self):
        obj_payslip = self.pool.get('hr.payslip')
        obj_line = self.pool.get('hr.payslip.line')
        
        tanggal_mulai = '%s-01-01' % (str(self.tahun))
        tanggal_akhir = '%s-12-31' % (str(self.tahun))
        
        res = {}
        res1 = {}
        kode = []
        
        kriteria = [('tanggal_slip', '>=', tanggal_mulai),('tanggal_slip', '<=', tanggal_akhir),('employee_id','=',self.karyawan_id)]
        payslip_ids = obj_payslip.search(self.cr, self.uid, kriteria)

        for slip in obj_payslip.browse(self.cr, self.uid, payslip_ids):
            for line in slip.detail_pendapatan_teratur_ids:
                if not res1.get(line.salary_rule_id.code, False):
                    res1[line.salary_rule_id.code] =           {
                                                'kode' : line.salary_rule_id.code,
                                                'ketentuan' : line.name,
                                                '01' : line.slip_id.tanggal_slip[5:7] == '01' and line.total or 0.0,
                                                '02' : line.slip_id.tanggal_slip[5:7] == '02' and line.total or 0.0,
                                                '03' : line.slip_id.tanggal_slip[5:7] == '03' and line.total or 0.0,
                                                '04' : line.slip_id.tanggal_slip[5:7] == '04' and line.total or 0.0,
                                                '05' : line.slip_id.tanggal_slip[5:7] == '05' and line.total or 0.0,
                                                '06' : line.slip_id.tanggal_slip[5:7] == '06' and line.total or 0.0,
                                                '07' : line.slip_id.tanggal_slip[5:7] == '07' and line.total or 0.0,
                                                '08' : line.slip_id.tanggal_slip[5:7] == '08' and line.total or 0.0,
                                                '09' : line.slip_id.tanggal_slip[5:7] == '09' and line.total or 0.0,
                                                '10' : line.slip_id.tanggal_slip[5:7] == '10' and line.total or 0.0,
                                                '11' : line.slip_id.tanggal_slip[5:7] == '11' and line.total or 0.0,
                                                '12' : line.slip_id.tanggal_slip[5:7] == '12' and line.total or 0.0,
                                                }
                else:
                    res1[line.salary_rule_id.code][line.slip_id.tanggal_slip[5:7]] += line.total
                    
            for line in slip.detail_pendapatan_tidak_teratur_ids:
                if not res1.get(line.salary_rule_id.code, False):
                    res1[line.salary_rule_id.code] =           {
                                                'kode' : line.salary_rule_id.code,
                                                'ketentuan' : line.name,
                                                '01' : line.slip_id.tanggal_slip[5:7] == '01' and line.total or 0.0,
                                                '02' : line.slip_id.tanggal_slip[5:7] == '02' and line.total or 0.0,
                                                '03' : line.slip_id.tanggal_slip[5:7] == '03' and line.total or 0.0,
                                                '04' : line.slip_id.tanggal_slip[5:7] == '04' and line.total or 0.0,
                                                '05' : line.slip_id.tanggal_slip[5:7] == '05' and line.total or 0.0,
                                                '06' : line.slip_id.tanggal_slip[5:7] == '06' and line.total or 0.0,
                                                '07' : line.slip_id.tanggal_slip[5:7] == '07' and line.total or 0.0,
                                                '08' : line.slip_id.tanggal_slip[5:7] == '08' and line.total or 0.0,
                                                '09' : line.slip_id.tanggal_slip[5:7] == '09' and line.total or 0.0,
                                                '10' : line.slip_id.tanggal_slip[5:7] == '10' and line.total or 0.0,
                                                '11' : line.slip_id.tanggal_slip[5:7] == '11' and line.total or 0.0,
                                                '12' : line.slip_id.tanggal_slip[5:7] == '12' and line.total or 0.0,
                                                }
                else:
                    res1[line.salary_rule_id.code][line.slip_id.tanggal_slip[5:7]] += line.total  
                    
            for line in slip.detail_potongan_ids:
                if not res1.get(line.salary_rule_id.code, False):
                    res1[line.salary_rule_id.code] =           {
                                                'kode' : line.salary_rule_id.code,
                                                'ketentuan' : line.name,
                                                '01' : line.slip_id.tanggal_slip[5:7] == '01' and line.total or 0.0,
                                                '02' : line.slip_id.tanggal_slip[5:7] == '02' and line.total or 0.0,
                                                '03' : line.slip_id.tanggal_slip[5:7] == '03' and line.total or 0.0,
                                                '04' : line.slip_id.tanggal_slip[5:7] == '04' and line.total or 0.0,
                                                '05' : line.slip_id.tanggal_slip[5:7] == '05' and line.total or 0.0,
                                                '06' : line.slip_id.tanggal_slip[5:7] == '06' and line.total or 0.0,
                                                '07' : line.slip_id.tanggal_slip[5:7] == '07' and line.total or 0.0,
                                                '08' : line.slip_id.tanggal_slip[5:7] == '08' and line.total or 0.0,
                                                '09' : line.slip_id.tanggal_slip[5:7] == '09' and line.total or 0.0,
                                                '10' : line.slip_id.tanggal_slip[5:7] == '10' and line.total or 0.0,
                                                '11' : line.slip_id.tanggal_slip[5:7] == '11' and line.total or 0.0,
                                                '12' : line.slip_id.tanggal_slip[5:7] == '12' and line.total or 0.0,
                                                }
                else:
                    res1[line.salary_rule_id.code][line.slip_id.tanggal_slip[5:7]] += line.total   
                    
            for line in slip.detail_asuransi_ids:
                if not res1.get(line.salary_rule_id.code, False):
                    res1[line.salary_rule_id.code] =           {
                                                'kode' : line.salary_rule_id.code,
                                                'ketentuan' : line.name,
                                                '01' : line.slip_id.tanggal_slip[5:7] == '01' and line.total or 0.0,
                                                '02' : line.slip_id.tanggal_slip[5:7] == '02' and line.total or 0.0,
                                                '03' : line.slip_id.tanggal_slip[5:7] == '03' and line.total or 0.0,
                                                '04' : line.slip_id.tanggal_slip[5:7] == '04' and line.total or 0.0,
                                                '05' : line.slip_id.tanggal_slip[5:7] == '05' and line.total or 0.0,
                                                '06' : line.slip_id.tanggal_slip[5:7] == '06' and line.total or 0.0,
                                                '07' : line.slip_id.tanggal_slip[5:7] == '07' and line.total or 0.0,
                                                '08' : line.slip_id.tanggal_slip[5:7] == '08' and line.total or 0.0,
                                                '09' : line.slip_id.tanggal_slip[5:7] == '09' and line.total or 0.0,
                                                '10' : line.slip_id.tanggal_slip[5:7] == '10' and line.total or 0.0,
                                                '11' : line.slip_id.tanggal_slip[5:7] == '11' and line.total or 0.0,
                                                '12' : line.slip_id.tanggal_slip[5:7] == '12' and line.total or 0.0,
                                                }
                else:
                    res1[line.salary_rule_id.code][line.slip_id.tanggal_slip[5:7]] += line.total 
                    
            for line in slip.detail_pensiun_ids:
                if not res1.get(line.salary_rule_id.code, False):
                    res1[line.salary_rule_id.code] =           {
                                                'kode' : line.salary_rule_id.code,
                                                'ketentuan' : line.name,
                                                '01' : line.slip_id.tanggal_slip[5:7] == '01' and line.total or 0.0,
                                                '02' : line.slip_id.tanggal_slip[5:7] == '02' and line.total or 0.0,
                                                '03' : line.slip_id.tanggal_slip[5:7] == '03' and line.total or 0.0,
                                                '04' : line.slip_id.tanggal_slip[5:7] == '04' and line.total or 0.0,
                                                '05' : line.slip_id.tanggal_slip[5:7] == '05' and line.total or 0.0,
                                                '06' : line.slip_id.tanggal_slip[5:7] == '06' and line.total or 0.0,
                                                '07' : line.slip_id.tanggal_slip[5:7] == '07' and line.total or 0.0,
                                                '08' : line.slip_id.tanggal_slip[5:7] == '08' and line.total or 0.0,
                                                '09' : line.slip_id.tanggal_slip[5:7] == '09' and line.total or 0.0,
                                                '10' : line.slip_id.tanggal_slip[5:7] == '10' and line.total or 0.0,
                                                '11' : line.slip_id.tanggal_slip[5:7] == '11' and line.total or 0.0,
                                                '12' : line.slip_id.tanggal_slip[5:7] == '12' and line.total or 0.0,
                                                }
                else:
                    res1[line.salary_rule_id.code][line.slip_id.tanggal_slip[5:7]] += line.total                                                                             
 
                
        for nilai in res1.itervalues():
            res =   {
                    'kode' : nilai['kode'],
                    'ketentuan' : nilai['ketentuan'],
                    '01' : nilai['01'],
                    '02' : nilai['02'],
                    '03' : nilai['03'],
                    '04' : nilai['04'],
                    '05' : nilai['05'],
                    '06' : nilai['06'],
                    '07' : nilai['07'],
                    '08' : nilai['08'],
                    '09' : nilai['09'],
                    '10' : nilai['10'],
                    '11' : nilai['11'],
                    '12' : nilai['12'],
                    'total' : nilai['01'] + nilai['02'] + nilai['03'] + nilai['04'] + nilai['04'] + nilai['05'] + nilai['06'] + nilai['07'] + nilai['08'] + nilai['09'] + nilai['10'] + nilai['11'] + nilai['12'],
                    }
                 
        
            self.isi_laporan.append(res)
    
        return self.isi_laporan
        
        
    def get_nama_karyawan(self):
        obj_karyawan = self.pool.get('hr.employee')
        karyawan_id = self.karyawan_id
        
        karyawan = obj_karyawan.browse(self.cr, self.uid, [karyawan_id])[0]
        
        return karyawan.name
        
    def get_nip_karyawan(self):
        obj_karyawan = self.pool.get('hr.employee')
        karyawan_id = self.karyawan_id
        
        karyawan = obj_karyawan.browse(self.cr, self.uid, [karyawan_id])[0]
        
        return karyawan.nip
        
    def get_tahun_laporan(self):
        
        return self.tahun 
        
    def get_payslip_ids(self):
        
        return str(self.slip_ids)
        
        
    def set_context(self, objects, data, ids, report_type=None):
        self.karyawan_id = data['form']['karyawan_id']
        self.tahun = data['form']['tahun']
        

        return super(riwayat_pembayaran_gaji, self).set_context(objects, data, ids, report_type=report_type)           

report_sxw.report_sxw('report.hr.riwayat_pembayaran_gaji', 'hr.payslip', 'addons/ar_hr_payroll/report/riwayat_pembayaran_gaji.rml', parser=riwayat_pembayaran_gaji, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


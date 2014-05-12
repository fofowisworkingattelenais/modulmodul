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
from datetime import datetime


class wizard_karyawan_baru(osv.osv_memory):
    _name = 'hr.wizard_karyawan_baru'
    _inherit = 'hr.wizard_karyawan_baru'


    _columns =  {
                'pn_kumulatif_sebelum' : fields.float('PN Kumulatif', Digits=(16,2)),
                'pph_kumulatif_sebelum' : fields.float('PPH 21 Kumulatif', Digits=(16,2)),
                }
                
    def buat_riwayat(self, cr, uid, ids, context={}):
        obj_wizard_karyawan_baru = self.pool.get('hr.wizard_karyawan_baru')
        obj_contract = self.pool.get('hr.contract')
        obj_mode_data = self.pool.get('ir.model.data')
        obj_karyawan = self.pool.get('hr.employee')
        
        tipe_history_id = obj_mode_data.get_object_reference(cr, uid, 'ar_hr_kontrak', 'data_tipeHistory_karyawanBaru')        
        
        wizard_karyawan_baru = obj_wizard_karyawan_baru.browse(cr, uid, ids, context)[0]
        
        res =   {
                'name' : '/',
                'employee_id' : wizard_karyawan_baru.employee_id.id,
                'company_id' : wizard_karyawan_baru.company_id.id,
                'department_id' : wizard_karyawan_baru.department_id.id,
                'job_id' : wizard_karyawan_baru.job_id.id,
                'manager_id' : wizard_karyawan_baru.manager_id and wizard_karyawan_baru.manager_id.id or False,
                'type_id' : wizard_karyawan_baru.tipe_kontrak_id.id,
                'wage' : wizard_karyawan_baru.wage,
                'struct_id' : wizard_karyawan_baru.struct_id.id,
                'periode_gaji_id' : wizard_karyawan_baru.periode_gaji_id.id,
                'tipe_history_id' : tipe_history_id[1],
                }
                
        obj_karyawan.write(cr, uid, [wizard_karyawan_baru.employee_id.id], {'pn_kumulatif_sebelum' : wizard_karyawan_baru.pn_kumulatif_sebelum, 'pph_kumutalif_sebelum' : wizard_karyawan_baru.pph_kumulatif_sebelum})
                
        if wizard_karyawan_baru.opsi_mulai == 'jadwal':
            res.update({'tanggal_mulai' : wizard_karyawan_baru.tanggal_mulai_history, 'mulai_otomatis' : True})        
                
        kontrak_id = obj_contract.create(cr, uid, res, context)
        
        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_validate(uid, 'hr.contract', kontrak_id, 'button_disetujui', cr)

        if wizard_karyawan_baru.opsi_mulai == 'segera':
            wkf_service.trg_validate(uid, 'hr.contract', kontrak_id, 'button_valid', cr)
        
        return {'type': 'ir.actions.act_window_close'}
        
    def batal(self, cr, uid, ids, context={}):
        return {'type': 'ir.actions.act_window_close'}
        
        
                
wizard_karyawan_baru()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

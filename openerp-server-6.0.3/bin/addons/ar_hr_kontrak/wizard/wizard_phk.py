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


class wizard_phk(osv.osv_memory):
    _name = 'hr.wizard_phk'
    _description = 'Wizard PHK'


    _columns =  {
                'employee_id' : fields.many2one('hr.employee', 'Karyawan', domain=['|', '|', ('status_karyawan','=','kontrak'),('status_karyawan','=','probation'),('status_karyawan','=','tetap')], required=True),
                'opsi_mulai' : fields.selection([('segera','Segera'),('jadwal','Jadwal'),('manual','Manual')], 'Opsi Mulai History', required=True),
                'tanggal_mulai_history' : fields.date('Tanggal Mulai Berlaku'),                   
                }
                
    def buat_riwayat(self, cr, uid, ids, context={}):
        obj_wizard_phk = self.pool.get('hr.wizard_phk')
        obj_contract = self.pool.get('hr.contract')
        obj_model_data = self.pool.get('ir.model.data')
        
        
        tipe_history_id = obj_model_data.get_object_reference(cr, uid, 'ar_hr_kontrak', 'data_tipeHistory_phk')
        wizard_phk = obj_wizard_phk.browse(cr, uid, ids)[0]
        
        kontrak_id = wizard_phk.employee_id.contract_id.id
        
        res =   {
                'name' : '/',
                'state' : 'draft',
                'tipe_history_id' : tipe_history_id[1],
                }
                
        if wizard_phk.opsi_mulai == 'jadwal':
            res.update({'tanggal_mulai' : wizard_phk.tanggal_mulai_history, 'mulai_otomatis' : True})                
                
        kontrak_baru_id = obj_contract.copy(cr, uid, kontrak_id, res, context)
        
        wkf_service = netsvc.LocalService('workflow')
        
        
        if wizard_phk.opsi_mulai == 'segera':
            wkf_service.trg_validate(uid, 'hr.contract', kontrak_baru_id, 'button_valid', cr)  
        
        
        return {}        
                
wizard_phk()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

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


class wizard_buat_timesheet(osv.osv_memory):
    _name = 'hr.wizard_buat_timesheet'
    _description = 'Wizard Buat Timesheet'


    _columns =  {
                'periode_kerja_id' : fields.many2one(obj='hr.periode_gaji', string='Periode Kerja', required=True),
                'detail_periode_kerja_id' : fields.many2one(obj='hr.detail_periode_gaji', string='Detail Periode Kerja', required=True),
                }
                
    def jalankan_wizard(self, cr, uid, ids, context={}):
        obj_wizard = self.pool.get('hr.wizard_buat_timesheet')
        obj_history = self.pool.get('hr.contract')   
        obj_timesheet = self.pool.get('hr.timesheet_karyawan')     
        
        wizard = obj_wizard.browse(cr, uid, ids)[0]
        
        kriteria = [('state','=','valid'),('periode_gaji_id','=',wizard.periode_kerja_id.id)]
        history_ids = obj_history.search(cr, uid, kriteria)
        
        for history in obj_history.browse(cr, uid, history_ids):
            kriteria_1 = [('employee_id','=',history.employee_id.id),('detail_periode_kerja_id','=',wizard.detail_periode_kerja_id.id)]
            timesheet_ids = obj_timesheet.search(cr, uid, kriteria_1)
            if not timesheet_ids:
                val =   {
                        'employee_id' : history.employee_id.id,
                        'pola_kerja_id' : history.pola_kerja_id.id,
                        'detail_periode_kerja_id' : wizard.detail_periode_kerja_id.id,
                        }
                        
                timesheet_id = obj_timesheet.create(cr, uid, val)
                
                obj_timesheet.buat_absensi(cr, uid, [timesheet_id])
  
        return {}        
                
wizard_buat_timesheet()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

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
import csv
import tools
import base64
from tempfile import TemporaryFile


class wizard_import_data_payroll(osv.osv_memory):
    _name = 'hr.wizard_import_data_payroll'
    _description = 'Wizard Import Data Payroll'


    _columns =  {
                'data_payroll' : fields.binary('Data Payroll'),
                'file_data_payroll' : fields.char('File Data Payroll',size=256),
                }
                
    def import_data_payroll(self, cr, uid, ids, context={}):
        obj_wizard = self.pool.get('hr.wizard_import_data_payroll')
        obj_import_data_payroll = self.pool.get('hr.import_data_payroll')
        obj_detail = self.pool.get('hr.import_detail_payslip_input')
        
        import_data = obj_wizard.browse(cr, uid, ids)[0]
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(import_data.data_payroll))
        fileobj.seek(0)
        reader = csv.DictReader(fileobj, delimiter=';')
        
        # raise osv.except_osv('a', str(context['active_ids']))
        
        for baris in reader:
            #raise osv.except_osv('a', str(baris))
            employee_id = baris['employee_id']
            for var in reader.fieldnames[1:]:
                kriteria = [('employee_id','=',int(employee_id)),('kode','=',var),('import_payslip_input_id','=',context['active_ids'][0])]
                #raise osv.except_osv('a', str(kriteria))
                detail_ids = obj_detail.search(cr, uid, kriteria)
                
                if detail_ids:
                    res =   {
                            'jumlah' : baris[var],
                            }
                            
                    obj_detail.write(cr, uid, [detail_ids[0]], res)
                elif not detail_ids:
                    res =   {
                            'employee_id' : employee_id,
                            'import_payslip_input_id' : context['active_ids'][0],
                            'kode' : var,
                            'jumlah' : baris[var],
                            }
                            
                    obj_detail.create(cr, uid, res)
                
            
        fileobj.close()
            
        return {}
            
        

        
    def batal(self, cr, uid, ids, context={}):
        return {'type': 'ir.actions.act_window_close'}
        
        
                
wizard_import_data_payroll()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

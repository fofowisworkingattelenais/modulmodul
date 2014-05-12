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


class wizard_cetak_riwayat_pembayaran_gaji(osv.osv_memory):
    _name = 'hr.wizard_cetak_riwayat_pembayaran_gaji'
    _description = 'Wizard Cetak Riwayat Pembayaran Gaji'
    
    def default_tahun(self, cr, uid, context={}):
        return datetime.today().year


    _columns =  {
                'employee_id' : fields.many2one(obj='hr.employee', string='Karyawan', required=True, domain=['|','|',('status_karyawan','=','tetap'),('status_karyawan','=','kontrak'),('status_karyawan','=','probation')]),
                'tahun' : fields.integer(string='Tahun', required=True),
                }
                
    _defaults = {
                'tahun' : default_tahun,
                }
                
    def cetak_laporan(self, cr, uid, ids, data, context=None):
	    if context is None:
		    context = {}
		
	    data = {}	
	    
	    wizard = self.browse(cr, uid, ids, context)[0]
	    
	    res =   {
	            'karyawan_id' : wizard.employee_id.id,
	            'tahun' : wizard.tahun,
	            }
	    
	    
	    data['form'] = res
	
	    return	{
			    'type': 'ir.actions.report.xml',
			    'report_name': 'hr.riwayat_pembayaran_gaji',
			    'datas': data,
			    }   
                
wizard_cetak_riwayat_pembayaran_gaji()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

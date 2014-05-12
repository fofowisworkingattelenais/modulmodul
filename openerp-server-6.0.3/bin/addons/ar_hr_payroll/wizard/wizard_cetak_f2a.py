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


class wizard_cetak_f2a(osv.osv_memory):
    _name = 'hr.wizard_cetak_f2a'
    _description = 'Wizard Cetak F2a'


    _columns =  {
                'bulan_id' : fields.many2one(string='Bulan', obj='base.bulan', required=True),
                'tahun' : fields.integer(string='Tahun', required=True),
                }
                

        
        
                
wizard_cetak_f2a()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

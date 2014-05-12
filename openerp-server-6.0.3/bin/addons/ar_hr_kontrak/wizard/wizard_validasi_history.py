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

import wizard
from osv import fields, osv
from datetime import date
import netsvc
from tools.translate import _


class wizard_validasi_history(osv.osv_memory):
	_name = 'hr.wizard_validasi_history'
	_description = 'Wizard Validasi History'


	def validasi_history(self, cr, uid, ids, context=None):
		obj_history = self.pool.get('hr.contract')
		wf_service = netsvc.LocalService('workflow')
		for id in ids:
			wf_service.trg_validate(uid, 'hr.contract', id, 'button_valid', cr)	
			
		return {'type': 'ir.actions.act_window_close'}
				
wizard_validasi_history()



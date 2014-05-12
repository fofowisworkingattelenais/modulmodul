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


class wizard_cancel_taxform_sequence(osv.osv_memory):
	_name = 'account.wizard_cancel_taxform_sequence'
	_description = 'Wizard Cancel Taxform Sequence'


	def cancel_sequence(self, cr, uid, ids, context=None):
		obj_taxform = self.pool.get('account.taxform')
		obj_sequence = self.pool.get('ir.sequence')
		obj_taxform_sequence = self.pool.get('account.taxform_sequence')
		
		for taxform in obj_taxform.browse(cr, uid, context['active_ids']):
			pass				
		return {'type': 'ir.actions.act_window_close'}
				
wizard_cancel_taxform_sequence()



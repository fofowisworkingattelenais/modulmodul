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


class wizard_select_taxform_sequence(osv.osv_memory):
	_name = 'account.wizard_select_taxform_sequence'
	_description = 'Wizard Select Taxform Sequence'
	
	def default_sequence_id(self, cr, uid, context={}):
		obj_taxform = self.pool.get('account.taxform')
		
		taxform = obj_taxform.browse(cr, uid, [context['active_id']])[0]
		
		if taxform.invoice_id.company_id.company_tax_id:
			sequence_id = taxform.invoice_id.company_id.company_tax_id.sequence_taxform_id.id
		else:
			sequence_id = taxform.invoice_id.company_id.sequence_taxform_id.id
			
		return sequence_id
	
	_columns = 	{
				'taxform_sequence_id' : fields.many2one(obj='account.taxform_sequence', string='Taxform ID'),
				'sequence_id' : fields.many2one(obj='ir.sequence', string='Sequence'),
				}
				
	_defaults =	{
				'sequence_id' : default_sequence_id,
				}


	def select_sequence(self, cr, uid, ids, context=None):
		obj_taxform = self.pool.get('account.taxform')
		obj_sequence = self.pool.get('account.taxform_sequence')
		obj_wizard = self.pool.get('account.wizard_select_taxform_sequence')
		
		wizard = obj_wizard.browse(cr, uid, ids, context)[0]
		
		#raise osv.except_osv('a', str(wizard.taxform_sequence_id.name))
		
		
		obj_taxform.write(cr, uid, [context['active_id']], {'name' : wizard.taxform_sequence_id.name, 'state':'printed'})
		obj_sequence.write(cr, uid, [wizard.taxform_sequence_id.id], {'taxform_id' : context['active_id']})
		
		
			
		return {'type': 'ir.actions.act_window_close'}
				
wizard_select_taxform_sequence()



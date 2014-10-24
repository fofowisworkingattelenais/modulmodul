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


from osv import fields, osv
from datetime import date
import netsvc
from tools.translate import _


class wizard_create_taxform_sequence(osv.osv_memory):
	_name = 'account.wizard_create_taxform_sequence'
	_description = 'Wizard Create Taxform Sequence'


	def create_sequence(self, cr, uid, ids, context=None):
		obj_taxform = self.pool.get('account.taxform')
		obj_sequence = self.pool.get('ir.sequence')
		obj_taxform_sequence = self.pool.get('account.taxform_sequence')
		
		for taxform in obj_taxform.browse(cr, uid, context['active_ids']):
			if taxform.invoice_id.company_id.company_tax_id:
				sequence_id = taxform.invoice_id.company_id.company_tax_id.sequence_taxform_id and taxform.invoice_id.company_id.company_tax_id.sequence_taxform_id.id or False
			else:
				sequence_id = taxform.invoice_id.company_id.sequence_taxform_id and taxform.invoice_id.company_id.sequence_taxform_id.id or False
				
			if not sequence_id:
				raise osv.except_osv('Warning!', 'No taxform sequence defined')
				
				
			sequence = obj_sequence.get_id(cr, uid, sequence_id, 'id', {'period_id':False})
			
			obj_taxform.write(cr, uid, [taxform.id], {'name':sequence, 'state':'printed'})
			
			val_sequence =	{
							'name' : sequence,
							'taxform_id' : taxform.id,
							'sequence_id' : sequence_id,
							}
			obj_taxform_sequence.create(cr, uid, val_sequence)
							
		return {'type': 'ir.actions.act_window_close'}
				
wizard_create_taxform_sequence()



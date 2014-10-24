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


class wizard_print_taxform_preprinted(osv.osv_memory):
	_name = 'account.wizard_print_taxform_preprinted'
	_description = 'Wizard Print Taxform Pre-Printed'
		



	def print_taxform(self, cr, uid, ids, context=None):
		datas = {}
		if context is None:
			context = {}
			
		data = self.read(cr, uid, ids, [], context)[0]
		
		datas =	{
				'ids' : context.get('active_ids', []),
				'model' : 'account.taxform',
				'form' : data
				}
				
		return	{
				'type' : 'ir.actions.report.xml',
				'report_name' : 'account.taxform.preprinted',
				'datas' : datas
				}

				
wizard_print_taxform_preprinted()



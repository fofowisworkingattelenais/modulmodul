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

class res_company(osv.osv):
	_name = 'res.company'
	_inherit = 'res.company'
	_columns = 	{
				'sequence_gaji_id' : fields.many2one('ir.sequence', 'Sequence Slip Gaji'),
				'sequence_batch_gaji_id' : fields.many2one('ir.sequence', 'Sequence Batch Slip Gaji'),
				'sequence_gaji_nonreguler_id' : fields.many2one('ir.sequence', 'Sequence Slip Gaji Non-Reguler'),
				'sequence_import_variabel_id' : fields.many2one('ir.sequence', 'Sequence Import Variabel'),
				'komponen_jamsostek_ids' : fields.many2many('hr.salary.rule', 'res_company_jamsostek_rel', 'salary_rule_id', 'company_id', 'Komponen Jamsostek'),
				}
res_company()




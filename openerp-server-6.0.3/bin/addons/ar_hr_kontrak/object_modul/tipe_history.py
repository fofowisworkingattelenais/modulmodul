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


class tipe_history(osv.osv):
	_name = 'hr.tipe_history'
	_description = 'Tipe History'

	def default_active(self, cr, uid, context={}):
		return 1
		
	_columns = 	{
				'name' : fields.char('Tipe History', size=100, required=True),
				'kode' : fields.char('Kode', size=30, required=True),
				'active' : fields.boolean('Aktif'),
				'ubah_status' : fields.char('Ubah Status Karyawan', size=30),
				'keterangan' : fields.text('Keterangan'),
				'kode_python' : fields.text(string='Kode Python'),
				'kode_python_karyawan' : fields.text(string='Kode Python Karyawan'),
				'field_copy_ids' : fields.many2many('ir.model.fields', 'rel_tipe_history_field', 'tipe_history_id', 'field_id', 'Field Yang Dicopy Dari History Sebelumnya', domain=[('model_id.model','=','hr.contract')])
				}
				
	_defaults =	{
				'active' : default_active,
				}

tipe_history()

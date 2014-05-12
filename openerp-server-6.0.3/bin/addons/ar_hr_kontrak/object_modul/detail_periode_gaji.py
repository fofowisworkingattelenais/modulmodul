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


class detail_periode_gaji(osv.osv):
	_name = 'hr.detail_periode_gaji'
	_description = 'Periode Gaji'

	def default_state(self, cr, uid, context={}):
		return 'draft'
		
	_columns = 	{
				'name' : fields.char('Periode Gaji', size=30, required=True),
				'periode_gaji_id' : fields.many2one('hr.periode_gaji', 'Periode Gaji', required=True),
				'tanggal_mulai' : fields.date('Tanggal Mulai', required=True),
				'tanggal_akhir' : fields.date('Tanggal Akhir', required=True),
				'state' : fields.selection([('draft','Draft'),('aktif','Aktif'),('selesai','Selesai')], 'Status', required=True, readonly=True),
				}
				
	_defaults =	{
				'state' : default_state,
				}
				
	def workflow_action_aktif(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'aktif'})
		return True
		
	def workflow_action_selesai(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'state' : 'selesai'})
		return True					

detail_periode_gaji()

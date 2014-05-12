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

class ir_sequence(osv.osv):
	_name = 'ir.sequence'
	_inherit = 'ir.sequence'
	
	def get_id(self, cr, uid, sequence_id, test='id', context=None):
		obj_bulan = self.pool.get('base.bulan')

		if context is None:
			context = {}

		tahun = False
		bulan_id = False
		tanggal = context.get('tanggal', False)

		if tanggal:
			tahun = tanggal[0:4]

			kode_bulan = tanggal[5:7]
			kriteria = [('kode','=',kode_bulan)]
			bulan_ids = obj_bulan.search(cr, uid, kriteria)

			if bulan_ids:
				bulan_id = bulan_ids[0]
				bulan = obj_bulan.browse(cr, uid, [bulan_id])[0]

			for sequence in self.browse(cr, uid, [sequence_id], context):
				if sequence.sequence_bulanan_ids:
					for line in sequence.sequence_bulanan_ids:
						if line.tahun == int(tahun) and line.bulan_id.id == bulan.id:
							return super(ir_sequence, self).get_id(cr, uid, line.sequence_bulan_id.id, 'id', context)
		return super(ir_sequence, self).get_id(cr, uid, sequence_id, test, context)	

			

ir_sequence()





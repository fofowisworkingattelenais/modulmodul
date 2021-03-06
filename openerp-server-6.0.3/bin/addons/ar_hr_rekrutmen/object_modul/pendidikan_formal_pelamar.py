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

class pendidikan_formal_pelamar(osv.osv):
	_name = 'hr.pendidikan_formal_pelamar'
	_description = 'Pendidikan Formal Pelamar'
	
	_columns = 	{
				'pelamar_id' : fields.many2one('hr.pelamar', 'Pelamar', required = True),
				'name' : fields.many2one('pendidikan.jenjang_pendidikan', 'Jenjang Pendidikan'),
				'nama_sekolah' : fields.char('Nama Institusi Pendidikan', size=100, required=True),
				'urutan' : fields.char('Urutan', size=5, required=True),
				'tahun_masuk' : fields.integer('Tahun Masuk'),
				'tahun_selesai' : fields.integer('Tahun Selesai'),
				'gpa' : fields.float('GPA', Digits=(10,2)),
				'keterangan' : fields.text('Keterangan'),
				}	
		
	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(pendidikan_formal_pelamar, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(pendidikan_formal_pelamar, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi', 'aman')
		
		if situasi == 'aman':
			return super(pendidikan_formal_pelamar, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')		
			

pendidikan_formal_pelamar()





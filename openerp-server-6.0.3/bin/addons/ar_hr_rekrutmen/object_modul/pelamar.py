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


class pelamar(osv.osv):
	def default_state(self, cr, uid, context={}):
		hasil = 'pelamar'
		return hasil
		
	def default_kode(self, cr, uid, context={}):
		return '/'

	_name = 'hr.pelamar'
	_description = 'Pelamar'
	_columns = 	{
				'name' : fields.char('Nama', size=100, required=True),
				'kode' : fields.char('# Pelamar', size=30, readonly=True),
				'jenis_kelamin_id' : fields.many2one('identitas.jenis_kelamin','Jenis Kelamin', required=True),
				'ktp' : fields.char('KTP', size=100),
				'expired_ktp' : fields.date('Sampai Dengan'),
				'sim' : fields.char('SIM A', size=100),
				'expired_sim' : fields.date('Sampai Dengan'),
				'npwp' : fields.char('NPWP', size=100),
				'expired_npwp' : fields.date('Sampai Dengan'),
				'simb' : fields.char('SIM B', size=100),
				'expired_simb' : fields.date('Sampai Dengan'),	
				'simb1' : fields.char('SIM B1', size=100),
				'expired_simb1' : fields.date('Sampai Dengan'),
				'simb2' : fields.char('SIM B2', size=100),
				'expired_simb2' : fields.date('Sampai Dengan'),	
				'simc' : fields.char('SIM C', size=100),
				'expired_simc' : fields.date('Sampai Dengan'),	
				'passport' : fields.char('Passport', size=100),
				'expired_passport' : fields.date('Sampai Dengan'),	
				'kitas' : fields.char('Kitas', size=100),
				'expired_kitas' : fields.date('Sampai Dengan'),																				
				'tempat_lahir' : fields.char('Tempat Lahir', size=100),
				'tanggal_lahir' : fields.date('Tanggal Lahir'),
				'status_pernikahan_id' : fields.many2one('identitas.status_pernikahan', 'Status Pernikahan'),
				'agama_id' : fields.many2one('identitas.agama', 'Agama'),
				'etnis_id' : fields.many2one('identitas.etnis', 'Etnis'),
				'alamat' : fields.char('Alamat', size=255),
				'lamaran_ids' : fields.one2many('hr.lamaran', 'pelamar_id', 'Lamaran'),
				'nama_pasangan' : fields.char('Nama Pasangan', size=100),
				'tanggal_menikah' : fields.date('Tanggal Menikah'),
				'nama_ayah' : fields.char('Nama Ayah', size=100),
				'nama_ibu' : fields.char('Nama Ibu', size=100),
				'anak_ids' : fields.one2many('hr.anak_pelamar', 'pelamar_id', 'Anak'),	
				'pendidikan_formal_ids' : fields.one2many('hr.pendidikan_formal_pelamar', 'pelamar_id', 'Pendidikan Formal'),
				'pendidikan_non_formal_ids' : fields.one2many('hr.pendidikan_non_formal_pelamar', 'pelamar_id', 'Pendidikan Non-Formal'),							
				'state' : fields.selection([('pelamar','Pelamar'),('diterima','Diterima')], 'Status', readonly=True),
				}

	_defaults = {
				'state' : default_state,
				'kode' : default_kode,
				}
		
	def create(self, cr, uid, values, context={}):
		# Overriding method create
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi_create', 'aman')
		
		if situasi == 'aman':
			return super(pelamar, self).create(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa ditambahkan')
			
	def copy(self, cr, uid, id, default=None, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar copy data diatur oleh context
		
		situasi = context.get('situasi_copy', 'aman')
		
		if situasi == 'aman':
			return super(pelamar, self).copy(cr, uid, id, default, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dicopy')
			
	def unlink(self, cr, uid, ids, context={}):
		# Overriding method copy
		# Tujuan :
		# 1. Agar penghapusan data diatur oleh context
		
		situasi = context.get('situasi_unlink', 'aman')
		
		if situasi == 'aman':
			return super(pelamar, self).unlink(cr, uid, ids, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa dihapus')
			
	def write(self, cr, uid, values, context={}):
		# Overriding method write
		# Tujuan :
		# 1. Agar penginputan data diatur melalui context
		
		situasi = context.get('situasi_write', 'aman')
		
		if situasi == 'aman':
			return super(pelamar, self).write(cr, uid, values, context)
		else:
			raise osv.except_osv('Peringatan', 'Data tidak bisa diedit')	
		
	def buat_sequence(self, cr, uid, pelamar_id):
		obj_ir_sequence = self.pool.get('ir.sequence')
		obj_user = self.pool.get('res.users')
		obj_pelamar = self.pool.get('hr.pelamar')

		user = obj_user.browse(cr, uid, [uid])[0]

		pelamar = obj_pelamar.browse(cr, uid, [pelamar_id])[0]
		
		sequence_id = user.company_id.sequence_pelamar_id.id
		
		if not sequence_id:
			raise osv.except_osv('Peringatan', 'Sequence untuk pelamar belum diset')
			return False
			
		sequence = obj_ir_sequence.next_by_id(cr, uid, sequence_id)
		self.write(cr, uid, pelamar_id, {'kode' : sequence})
		return True	
		
	def create(self, cr, uid, values, context={}):
		pelamar_id = super(pelamar, self).create(cr, uid, values, context)
		
		if not self.buat_sequence(cr, uid, pelamar_id):
			return False
			
		return pelamar_id
		
pelamar()

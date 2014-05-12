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

class hr_employee(osv.osv):
	_name = 'hr.employee'
	_inherit = 'hr.employee'
	
	def default_status_karyawan(self, cr, uid, context={}):
		return 'draft'
	
	_columns =	{
				'nip' : fields.char('NIP', size=30),
				'ktp' : fields.char('KTP', size=30),
				'expired_ktp' : fields.date('Sampai Dengan'),
				'sim' : fields.char('SIM A', size=30),
				'expired_sim' : fields.date('Sampai Dengan'),
				'npwp' : fields.char('NPWP', size=30),
				'expired_npwp' : fields.date('Sampai Dengan'),
				'simb' : fields.char('SIM B', size=30),
				'expired_simb' : fields.date('Sampai Dengan'),
				'simb1' : fields.char('SIM B1', size=30),
				'expired_simb1' : fields.date('Sampai Dengan'),				
				'simb2' : fields.char('SIM B2', size=30),
				'expired_simb2' : fields.date('Sampai Dengan'),				
				'simc' : fields.char('SIM C', size=30),
				'expired_simc' : fields.date('Sampai Dengan'),
				'passport' : fields.char('Passport', size=30),
				'expired_passport' : fields.date('Sampai Dengan'),
				'kitas' : fields.char('Kitas', size=30),
				'expired_kitas' : fields.date('Sampai Dengan'),												
				'tanggal_lahir' : fields.date('Tanggal Lahir'),
				'tempat_lahir' : fields.char('Tempat Lahir', size=100),
				'jenis_kelamin_id' : fields.many2one('identitas.jenis_kelamin', 'Jenis Kelamin'),
				'agama_id' : fields.many2one('identitas.agama', 'Agama'),
				'etnis_id' : fields.many2one('identitas.etnis', 'Etnis'),
				'status_pernikahan_id' : fields.many2one('identitas.status_pernikahan', 'Status Pernikahan'),
				'status_karyawan' : fields.selection([('draft','Draft'),('probation','Probation'),('gagal_probation','Tidak Lulus Probation'),('kontrak','Karyawan Kontrak'),('tidak_diperpanjang','Kontrak Tidak Diperpanjang'),('tetap','Karyawan Tetap'),('phk','PHK'),('pensiun_dini','Pensiun Dini'),('pensiun','Pensiun'),('resign','Resign')], 'Status', readonly=True),
				}
				
	_defaults =	{
				'status_karyawan' : default_status_karyawan,
				}

			
	def workflow_action_probation(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'probation'})
			
		return True
		
	def workflow_action_kontrak(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'kontrak'})
			
		return True	
		
	def workflow_action_tetap(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'tetap'})
			
		return True			
		
	def workflow_action_gagalProbation(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'gagal_probation'})
			
		return True	
		
	def workflow_action_tidakDiperpanjang(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'tidak_diperpanjang'})
			
		return True				
		
	def workflow_action_phk(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'phk'})
			
		return True			
		
	def workflow_action_pensiunDini(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'pensiun_dini'})
			
		return True			
		
	def workflow_action_pensiun(self, cr, uid, ids, context={}):
		for id in ids:
			self.write(cr, uid, [id], {'status_karyawan' : 'tetap'})
			
		return True			
			

hr_employee()





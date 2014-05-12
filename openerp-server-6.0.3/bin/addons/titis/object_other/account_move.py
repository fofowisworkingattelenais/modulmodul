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
from datetime import datetime

class account_move(osv.osv):
	_name = 'account.move'
	_inherit = 'account.move'
	
	def default_originator_id(self, cr, uid, context={}):
		return uid
		
	def default_waktu_dibuat(self, cr, uid, context={}):
		return datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	
	_columns =	{
							'originator_id' : fields.many2one(obj='res.users', string='Originator', readonly=True),
							'waktu_dibuat' : fields.datetime(string='Created Time', readonly=True), 
							'otorisator_id' : fields.many2one(obj='res.users', string='Authorizator', readonly=True),
							'waktu_diotorisasi' : fields.datetime(string='Authorized Time', readonly=True),
							'verificator_id' : fields.many2one(obj='res.users', string='Verificator', readonly=True),
							'waktu_diverifikasi' : fields.datetime(string='Verified Time', readonly=True),
							'state': fields.selection([('draft','Draft'),('authorized','Authorized'), ('posted','Verified')], 'State', required=True, readonly=True),
							
							# diubah state nya
							'period_id': fields.many2one('account.period', 'Period', required=True, readonly=True, states={'draft':[('readonly',False)]}),
							'journal_id': fields.many2one('account.journal', 'Journal', required=True, readonly=True, states={'draft':[('readonly',False)]}),
							'line_id': fields.one2many('account.move.line', 'move_id', 'Entries', readonly=True, states={'draft':[('readonly',False)]}),
							'date': fields.date('Date', required=True, readonly=True, states={'draft':[('readonly',False)]}, select=True),
							
							}
							
	_defaults =	{
							'originator_id' : default_originator_id,
							'waktu_dibuat' : default_waktu_dibuat,
							}
							
	def button_validate(self, cr, uid, ids, context=None):
		"""
		Dijalankan oleh tombol Verified
		"""
		
		if super(account_move, self).button_validate(cr, uid, ids, context):
			val =	{
						'verificator_id' : uid,
						'waktu_diverifikasi' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
						}
						
			self.write(cr, uid, ids, val)
			return True
		else:
			return False
			
	def button_authorize(self, cr, uid, ids, context=None):
		"""
		Dijalankan oleh tombol Authorize
		"""
		val =	{
					'otorisator_id' : uid,
					'waktu_diotorisasi' : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
					'state' : 'authorized',
					}
		self.write(cr, uid, ids, val)			
			
			
							
account_move()							
							







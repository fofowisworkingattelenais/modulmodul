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


from osv import fields, osv

class product_product(osv.osv):
    _name = "product.product"
    _inherit = 'product.product'
    
    def default_currency_standard_id(self, cr, uid, context={}):
        obj_user = self.pool.get('res.users')
        
        user = obj_user.browse(cr, uid, [uid])[0]
        
        return user.company_id.currency_id.id
        
    def default_currency_list_id(self, cr, uid, context={}):
        obj_user = self.pool.get('res.users')
        
        user = obj_user.browse(cr, uid, [uid])[0]
        
        return user.company_id.currency_id.id        

    _columns = {
                'default_code' : fields.char(string='Part Number', size=64),
                'lenght' : fields.float(string='Lenght', digits=(16,2)),
                'width' : fields.float(string='Width', digits=(16,2)),
                'currency_standard_id' : fields.many2one(obj='res.currency', string='Cost Price Currency', required=True),
                'currency_list_id' : fields.many2one(obj='res.currency', string='Sale Price Currency', required=True),
            }
            
    _defaults = {
                            'currency_standard_id' : default_currency_standard_id,
                            'currency_list_id' : default_currency_list_id,
                            }

    _sql_constraints = [
            ('part_number_unik', 'unique(default_code)', 'Default Code must be unique !'),
    ]    
product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


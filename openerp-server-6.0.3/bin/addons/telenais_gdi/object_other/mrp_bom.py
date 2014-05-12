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

class mrp_bom(osv.osv):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'
    
    def function_lenght_dummy(self, cr, uid, ids, field_name, args, context=None):
	    res = {}
	    obj_line = self.pool.get('mrp.bom')
	
	    for line in obj_line.browse(cr, uid, ids):				
		    res[line.id] = line.lenght
		
	    return res
	
    def function_width_dummy(self, cr, uid, ids, field_name, args, context=None):
	    res = {}
	    obj_line = self.pool.get('mrp.bom')
	
	    for line in obj_line.browse(cr, uid, ids):				
		    res[line.id] = line.width
		
	    return res    

    _columns = {
                            'lenght' : fields.float(string='Lenght', digits=(16,2)),
                            'width' : fields.float(string='Width', digits=(16,2)),
                            'lenght_dummy' : fields.function(fnct=function_lenght_dummy, string='Lenght', type='float', digits=(16,2), method=True, store=False),
                            'width_dummy' : fields.function(fnct=function_width_dummy, string='Width', type='float', digits=(16,2), method=True, store=False),
            }
            
    def onchange_product_id(self, cr, uid, ids, product_id, name, context=None):
    
        obj_produk = self.pool.get('product.product')
        
        res = super(mrp_bom, self).onchange_product_id(cr, uid, ids, product_id, name, context)
        
        if product_id:
            produk = obj_produk.browse(cr, uid, [product_id])[0]
            res['value'].update({'lenght' : produk.lenght, 'lenght_dummy' : produk.lenght, 'width' : produk.width, 'width_dummy' : produk.width})
            
        return res
            
mrp_bom()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


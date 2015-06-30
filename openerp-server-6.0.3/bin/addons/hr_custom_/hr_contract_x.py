# -*- coding: utf-8 -*-
##############################################################################
#
#   Kustomsiasi modul hr_contract  
#
##############################################################################

from osv import fields, osv

import addons

#custom employee
class hr_contract(osv.osv):
    _inherit = "hr.contract"
    _columns = {
        'food_allounce': fields.float('Tunj. Makan', digits=(16,4), required=True),
        'food_allounce_deduct': fields.float('Pot. Tunj. Makan (%)', digits=(16,4), required=True),
        'trans_allounce': fields.float('Tunj. Transport', digits=(16,4), required=True),
        'trans_allounce_deduct': fields.float('Pot. Tunj. Transport (%)', digits=(16,4), required=True),
        'iuran_premi_kk': fields.float('Iuran Premi Kec. Kerja (%)', digits=(16,4), required=True),
        'iuran_premi_jk': fields.float('Iuran Premi Jam. Kematian (%)', digits=(16,4), required=True),
        'premi_jht': fields.float('Premi Jam. Hari Tua (%)', digits=(16,4), required=True),
        'tax_mode': fields.selection([('gross', 'Gross'),('gross_up', 'Gross Up')], 'Tax Mode', required=True),
    }

hr_contract() 
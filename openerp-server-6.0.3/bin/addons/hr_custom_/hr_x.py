# -*- coding: utf-8 -*-
##############################################################################
#
#   Kustomsiasi modul hr  
#
##############################################################################

from osv import fields, osv

import addons 

"""
pendapatan tidak kena pajak
"""
class hr_pph_ptkp(osv.osv):
    _name = "hr.pph.ptkp"
    _columns = {
        'name': fields.char('Name', size=32, required=True, translate=False),        
        'marital': fields.many2one('hr.employee.marital.status', 'Marital Status', required=True, select=True),         
        'ptkp': fields.float('Ptkp', digits=(16, 4), required=True),
        'desc': fields.char('Description', size=32, required=False, translate=False)
    }
    

hr_pph_ptkp()

"""
tarif progressif
"""
class hr_pph_tarif(osv.osv):
    _name = "hr.pph.tarif"
    _columns = {
        'tarif': fields.float('Rate (%)', digits=(16, 4), required=True),
        'pkp': fields.float('Pkp', digits=(16, 4), required=True),        
        'nonpwp_rate': fields.float('No Npwp Rate (%)', digits=(16, 4), required=True),
        'desc': fields.char('Description', size=32, required=False, translate=False)
    }
    __defaults = {
        'nonpwp_rate' : 0,
    }    

hr_pph_tarif()

"""
biaya jabatan
"""
class hr_pph_occupy_expense(osv.osv):
    _name = "hr.pph.occupy.expense"
    _columns = {
        'amount': fields.float('Biaya (%)', digits=(16, 4), required=True),
        'maximum': fields.float('Maximum', digits=(16, 4), required=True),        
        'desc': fields.char('Description', size=32, required=False, translate=False)
    }    

hr_pph_occupy_expense()


"""
salary head untuk pph
"""
class hr_pph_salary_head_pph(osv.osv):
    _name = "hr.pph.salary.head.pph"        
    _columns = {
        'category_id':fields.many2one('hr.allounce.deduction.categoty', 'Heads', required=True),        
        'desc': fields.char('Description', size=32, required=False, translate=False)
    }
    
hr_pph_salary_head_pph()


"""
salary head tunj pph
"""
class hr_pph_salary_head_pph_allow(osv.osv):
    _name = "hr.pph.salary.head.pph.allow"
    _inherit = "hr.pph.salary.head.pph"    

hr_pph_salary_head_pph_allow()

"""
salary head thr
"""
class hr_pph_salary_head_thr(osv.osv):
    _name = "hr.pph.salary.head.thr"
    _inherit = "hr.pph.salary.head.pph"    

hr_pph_salary_head_thr()


"""
custom employee
"""
class hr_employee(osv.osv):
    _inherit = "hr.employee"
    _columns = {
        'npwp': fields.char('Npwp', size=32, required=False, translate=False),
        'gol_ptkp': fields.many2one('hr.pph.ptkp', 'Golongan Ptkp', required=False, select=True),
    }
    __defaults = {
        'npwp' : lambda *a: '',
    }

hr_employee()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

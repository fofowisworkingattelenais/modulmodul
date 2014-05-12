# -*- coding: utf-8 -*-
##############################################################################
#
#   Kustomsiasi modul hr_timesheet_sheet  
#
##############################################################################

from osv import fields, osv
from datetime import datetime
import time
import addons 
import logging as log


class hr_attendance(osv.osv):
    _inherit = "hr.attendance"            
    _columns = {
        'source': fields.selection([
             ('manual','Manual Entry'),
            ('import','Imported'),
        ],'Source', select=True, required=True),        
    }
    __defaults = {
        'source': 'manual',    
    }
    
    #override
    def _altern_si_so(self, cr, uid, ids, context=None):
        for id in ids:
            for att in self.browse(cr, uid, [id], context=context):
                log.info("id=%d,att=%s,att.source=%s" % (id,att,att.source))
                if att.source == 'import': return True
                    
            sql = '''
            SELECT action, name, source
            FROM hr_attendance AS att
            WHERE employee_id = (SELECT employee_id FROM hr_attendance WHERE id=%s)
            AND action IN ('sign_in','sign_out')
            AND name <= (SELECT name FROM hr_attendance WHERE id=%s)
            ORDER BY name DESC
            LIMIT 2 '''
            cr.execute(sql,(id,id))
            atts = cr.fetchall()            
            if not ((len(atts)==1 and atts[0][0] == 'sign_in') or (len(atts)==2 and atts[0][0] != atts[1][0] and atts[0][1] != atts[1][1])):
                return False
        return True
    
    _constraints = [(_altern_si_so, 'Error: Sign in (resp. Sign out) must follow Sign out (resp. Sign in)', ['action'])]
    
hr_attendance()

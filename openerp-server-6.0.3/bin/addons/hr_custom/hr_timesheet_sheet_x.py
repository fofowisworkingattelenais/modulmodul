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
from tools.translate import _
import decimal_precision as dp

import logging as log


class hr_timesheet_sheet(osv.osv):
    _inherit = "hr_timesheet_sheet.sheet"
    
    def _get_total_duration(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        try:            
            duration = 0
            for sheet in self.browse(cr, uid, ids, context=context):            
                for overtime in sheet.overtime_ids:
                    duration += overtime.duration
                    
                res[sheet.id] = duration         
        except Exception, e:
            raise osv.except_osv(_('Variable Error !'), _('Variable Error: %s') % (e))
        
        return res
    
    _columns = {        
        'overtime_ids': fields.one2many('hr_timesheet_sheet.sheet.overtime', 'sheet_id', 'Overtime lines', readonly=False),
        'total_overtimes': fields.function(_get_total_duration, method=True, store=True, type='float', size=64, string='Total Duration', readonly=True),            
    }
    __defaults = {
        #'source': 'manual',    
    }
    

hr_timesheet_sheet()

class hr_timesheet_sheet_sheet_overtime(osv.osv):
    _name = "hr_timesheet_sheet.sheet.overtime"
    _description = "Overtimes"
    _order='start_time'    
    def _compute_duration(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        #log.info('_compute_duration')         
        for line in self.browse(cr, uid, ids, context=context):
            start_time = datetime.fromtimestamp(time.mktime(time.strptime(line.start_time,'%Y-%m-%d %H:%M:%S')))
            #log.info("start_time %s " % start_time)
            end_time = datetime.fromtimestamp(time.mktime(time.strptime(line.end_time,'%Y-%m-%d %H:%M:%S')))
            #log.info("end_time %s " % end_time)
            duration = (end_time - start_time).total_seconds() / 3600
            #log.info("duration %s " % duration)
            res[line.id] = duration            
        return res
        
    _columns = {
        'sheet_id': fields.many2one('hr_timesheet_sheet.sheet', 'Sheet', required=True, readonly=True, select="1"),       
        'start_time': fields.datetime('Start'),
        'end_time': fields.datetime('End'),
        'duration': fields.function(_compute_duration, method=True, store=True, type='float', size=64, string='Duration', readonly=True),
        'note': fields.text('Description') 
    }
    

hr_timesheet_sheet_sheet_overtime()


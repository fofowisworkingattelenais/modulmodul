# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
import time
import tools
import base64

from datetime import datetime
from tempfile import TemporaryFile, NamedTemporaryFile

from osv import osv, fields 
import logging as log

class hr_timesheet_import_message(osv.osv_memory):
    _name = 'hr.timesheet.import.message'
    _description = 'Message window'
    
class hr_timesheet_import_att_data(osv.osv_memory):
    _name = 'hr.timesheet.import.att.data'
    _description = 'Import data attendance'
    _columns= {
        #'sheet_id': fields.many2one('hr_timesheet_sheet.sheet', 'Sheet', required=True, select="1"),        
        'data': fields.binary('File')
    }     
    def _isnumeric(self, value):
        return str(value).replace(".","").replace("-","").isdigit()
    
    #skenario 1
    ###
    # data kehadiran dengan format 1 employee =  1 row berisi jam masuk dan jam keluar
    ###
    def _process_data_1(self, cr, uid, ids, data, context):
        #try:
            fileobj = TemporaryFile('w+')        
            fileobj.write(data)
            fileobj.seek(0) 
            lines = []
            for line in fileobj.readlines():
                #log.info('++++++++++++++++\r\nline=%s' % line)
                lines = line.split(',')            
                #if len(lines) == 0: break
                if self._isnumeric(lines[0]) == True:
                    id = int(lines[0])
                    date_from = datetime.strptime(lines[1], '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d  %H:%M:%S')
                    date_to = datetime.strptime(lines[2].replace("\n",""), '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d  %H:%M:%S')               
                    #log.info('id=%s,df=%s,dt=%s' % (id, date_from, date_to))
                    #check existing
                    day = datetime.strptime(date_from, '%Y-%m-%d  %H:%M:%S').strftime('%Y-%m-%d')
                    
                    attds = self.pool.get('hr.attendance')
                    attd_ids = attds.search(cr, uid, [('employee_id','=',id),('day','=',day)], context=context)
                    
                    #log.info(attd_ids)
                    log.info('employee_id=%d,attd_ids=%s,len=%d,day=%s' % (id,attd_ids,len(attd_ids), day))                                           
                    if len(attd_ids) == 0:                        
                        attds.create(cr, uid, {'employee_id':id,'name':date_from,'action':'sign_in','source':'import'})
                        attds.create(cr, uid, {'employee_id':id,'name':date_to,'action':'sign_out','source':'import'})
                #log.info('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            fileobj.close()
        #except:
        #    raise osv.except_osv('Message','Import failed!')
        
    #skenario 2
    ###
    # data kehadiran dengan format 2 row dengan row pertama berisi signin dan row berikutnya berisi sigout
    ###
    def _process_data_2(self, cr, uid, ids, data, context):
        #try:
            fileobj = TemporaryFile('w+')        
            fileobj.write(data)
            fileobj.seek(0)
            lines = []
            for line in fileobj.readlines():
                lines = line.split(',')            
                #if len(lines) == 0: break
                if self._isnumeric(lines[0]) == True:
                    id = int(lines[0])                
                    sign_date_new = datetime.strptime(lines[1].replace("\n",""), '%m/%d/%Y %H:%M:%S');
                    sign_date_str = sign_date_new.strftime('%Y-%m-%d %H:%M:%S')                           
                    #log.info('id=%s,date=%s' % (id, sign_date))                    
                    #check existing
                    day = sign_date_new.strftime('%Y-%m-%d')
                    
                    attds = self.pool.get('hr.attendance')
                    attd_ids = attds.search(cr, uid, [('employee_id','=',id),('day','=',day)], context=context)
                    
                    #log.info(attd_ids)
                    #log.info('employee_id=%d,attd_ids=%s,len=%d,day=%s' % (id,attd_ids,len(attd_ids), day))                                           
                    if len(attd_ids) == 0:
                        attds.create(cr, uid, {'employee_id':id,'name':sign_date_str,'action':'sign_in','source':'import'})
                    elif len(attd_ids) == 1:    
                        #check tgl sign dan action 
                        attd = attds.browse(cr, uid, attd_ids, context=context)
                        sign_date_old = datetime.strptime(attd[0].name, '%Y-%m-%d %H:%M:%S')
                        if sign_date_new > sign_date_old:  
                            attds.create(cr, uid, {'employee_id':id,'name':sign_date_str,'action':'sign_out','source':'import'})
                        else:
                            #update existing action from "sign_in" to "sign_out"
                            attds.write(cr, uid, [attd[0].id], {'action':'sign_out'})
                            #insert new 
                            attds.create(cr, uid, {'employee_id':id,'name':sign_date_str,'action':'sign_in','source':'import'})
                
            fileobj.close()
        #except:
        #    raise osv.except_osv('Message','Import failed!')
    
    def proccess_file(self, cr, uid, ids, context):
        #log.info('proccess_file')
        #try:            
            import_data = self.browse(cr, uid, ids)[0]            
            if import_data.data == False:
                raise osv.except_osv('Message','Please select .CSV file')
            #begin test
            """
            #format 1
            csv1 = 'employee_id.id,date_from,date_to\n'
            csv1 += '1,10/29/2013 08:00:00,10/29/2013 17:00:00\n'
            csv1 += '2,10/29/2013 07:45:02,10/29/2013 17:00:00\n'
            #format 2
            csv2 = 'employee_id.id,sign_date\n'                
            csv2 += '2,11/01/2013 07:45:02\n'
            csv2 += '2,11/01/2013 17:00:00\n'      
            csv2 += '2,11/02/2013 08:00:00\n'
            csv2 += '2,11/02/2013 17:00:00\n'
            
            csv2 += '2,11/03/2013 07:45:02\n'
            csv2 += '2,11/03/2013 17:00:00\n'      
            csv2 += '2,11/04/2013 08:00:00\n'
            csv2 += '2,11/04/2013 17:00:00\n'
            
            csv2 += '2,11/05/2013 08:00:00\n'
            csv2 += '2,11/05/2013 17:00:00\n'
            csv2 += '2,11/06/2013 08:00:00\n'
            csv2 += '2,11/06/2013 17:00:00\n'
            csv2 += '2,11/07/2013 08:00:00\n'
            csv2 += '2,11/07/2013 17:00:00\n'
            
            csv2 += '2,11/08/2013 08:00:00\n'
            csv2 += '2,11/08/2013 17:00:00\n'
            
            csv2 += '2,11/09/2013 08:00:00\n'
            csv2 += '2,11/09/2013 17:00:00\n'
            
            csv2 += '2,11/10/2013 08:00:00\n'
            csv2 += '2,11/10/2013 17:00:00\n'
            
            csv2 += '2,11/11/2013 08:00:00\n'
            csv2 += '2,11/11/2013 17:00:00\n'
            csv2 += '2,11/12/2013 09:00:00\n'
            csv2 += '2,11/12/2013 17:00:00\n'
            csv2 += '2,11/13/2013 08:00:00\n'
            csv2 += '2,11/13/2013 17:00:00\n'
            csv2 += '2,11/14/2013 08:00:00\n'
            csv2 += '2,11/14/2013 17:00:00\n'
            csv2 += '2,11/15/2013 08:10:00\n'
            csv2 += '2,11/15/2013 17:00:00\n'
            
            
            csv2 += '2,11/17/2013 08:10:00\n'
            csv2 += '2,11/17/2013 17:00:00\n'
            
            csv2 += '2,11/20/2013 17:00:00\n'
            csv2 += '2,11/16/2013 17:00:00\n'
            
            csv2 += '2,11/18/2013 08:10:00\n'
            csv2 += '2,11/18/2013 17:00:00\n'
            
            csv2 += '2,11/16/2013 08:10:00\n'
            
            csv2 += '2,11/19/2013 08:10:00\n'
            csv2 += '2,11/19/2013 17:00:00\n'
            
            csv2 += '2,11/20/2013 08:10:00\n'
            
            
            csv2 += '2,11/21/2013 08:10:00\n'
            csv2 += '2,11/21/2013 17:00:00\n'
            
            import_data.data = base64.encodestring(csv2)
            """
            #end test
                        
            data = base64.decodestring(import_data.data)
            #log.info('data=%s' % data)
            #process data        
            self._process_data_2(cr, uid, ids, data, context)
            
            return {'type': 'ir.actions.act_window_close'}
        #except Exception, e:
        #    raise osv.except_osv('Alert','Error %s ' % (e))
        
hr_timesheet_import_att_data()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
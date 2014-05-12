#-*- coding:utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    'name': 'Human Resource, Payroll Custom',
    'version': '1.8.2',
    'category': 'Generic Modules/Human Resources',
    'description': """Custom Payroll system
    * Custom Payroll
    * Custom Attendance
    """,
    'author':'zhufre@gmail.com',
    'website':'http://www.telenais.com',
    'depends': [
        'hr',        
        'hr_contract',        
        'hr_holidays',
        'hr_payroll',
        'hr_timesheet',
        'hr_timesheet_sheet',
        'decimal_precision',
    ],
    'init_xml': [
    ],
    'update_xml': [
        'hr_view_x.xml', 
        'hr_contract_view_x.xml', 
        'hr_payroll_view_x.xml',
        'hr_timesheet_sheet_view_x.xml', 
        'wizard/hr_timesheet_import_att_data_view.xml',
        ],
    'test': [
         
    ],    
    'demo_xml': [
        
    ],
    'installable': True,
    'active': False,
    'certificate' : '',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

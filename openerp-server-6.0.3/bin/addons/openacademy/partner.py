from osv import osv, fields

class Partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'instructor' : fields.boolean('Instructor'),
        'session_ids': fields.many2many('openacademy.session',
            'openacademy_attendee',
            'partner_id','session_id','Sessions')
    }

Partner()

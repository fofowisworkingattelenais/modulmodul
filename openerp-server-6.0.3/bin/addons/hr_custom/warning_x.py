from osv import fields, osv
import addons

w_types = [('info','Information'), ('warning','Warning'), ('error','Error')]

class warning_x():
    _columns = {
        'title': fields.char('Title', size=64, required=False, translate=False),
        'message': fields.text('Message')
    }
    
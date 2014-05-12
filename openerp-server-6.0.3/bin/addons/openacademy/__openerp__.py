{
        "name": "Open Academy",
        "version": "1.0",
        "depends": ["base", "board"],
        "author": "Author Name",
        "category": "Test",
        "description": """
        Open Academy module for managing trainings:
         - training courses
         - training sessions
         - attendees registration
        """,
        'data': [
            'openacademy_view.xml',
            'partner_view.xml',
            'board_session_view.xml',
            'openacademy_workflow.xml',
            'security/groups.xml',
            'security/ir.model.access.csv',
            'wizard/create_attendee_view.xml',
            'wizard/create_attendee_action.xml',
            'report/declare_report.xml',
        ],
        'demo': [],
        'installable': True,
        'active': False,
}

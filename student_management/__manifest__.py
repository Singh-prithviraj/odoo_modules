{
    'name': 'Student Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage students and courses',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/student_views.xml',
        'views/subject_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

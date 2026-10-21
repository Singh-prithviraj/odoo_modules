{
    'name': 'Academy Management',
    'version': '1.0',
    'summary': 'Academy Management System',
    'license': 'LGPL-3',
    'description': """
        Manage Courses, Batches, Students,
        Trainers and Enrollments.
    """,
    'category': 'Education',
    'author': 'Prithviraj',

    'depends': [
        'base',
        'contacts',
        'sale_management',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/batch_views.xml',
        'views/partner_views.xml',
        'views/student_views.xml',
        'views/enrollment_views.xml',
        'views/sale_order_views.xml',
    ],

    'installable': True,
    'application': True,
}

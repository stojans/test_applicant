{
    'name': 'Test Applicant Module',
    'version': '1.0',
    'category': 'Custom',
    'description': 'Custom Test Applicant module for managing applicants.',
    'author': 'Stefan',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/test_model_views.xml',
    ],
    'installable': True,
    'application': True,
}

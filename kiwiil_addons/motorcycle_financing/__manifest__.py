{
    "name": "Motorcycle Financing",
    "summary": "Streamlines the loan application process for dealerships.",
    "category": "Kawiil/Custom Modules",
    "version": "19.0.0.0.0",
    "website": "Repo GitHub",
    'depends': [
        'base',
        'product',      
        'sale_management',
    ],
    "author": "Dmarsiglia",
    "license": "OPL-1",
    "application": "True",
    # "demo": [
    #     'data/loan_demo.xml',
    # ],
    "data": [
        'security/motorcycle_financing_groups.xml',
       # 'security/loan_application_tags_groups.xml',
        'security/ir.model.access.csv',
        'views/loan_application_views.xml',
        'views/loan_application_tag.xml',
        'views/loan_document_type.xml',
        'views/motorcycle_financy_menu.xml',
        
    ],
}
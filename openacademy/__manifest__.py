{
    "name": "Open Academy",
    "version": "1.0",
    "summary": "Open Academy Training Module",
    "author": "Prithviraj",
    "category": "Training",
    "depends": ["base", "website"],
    "data": [
        "security/ir.model.access.csv",
        "views/course_views.xml",
        "views/session_views.xml",
        "views/menu.xml",
        "views/website_template.xml",
        # "views/practice_templates.xml"
        "views/partner_inherit_views.xml",

    ],
    "installable": True,
    "application": True,
}

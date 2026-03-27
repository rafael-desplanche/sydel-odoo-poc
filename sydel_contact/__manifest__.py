{
    "name": "Sydel Contacts",
    "version": "19.0.1.0.0",
    "summary": "Custom contact management for Sydel",
    "description": """
Sydel custom contact layer:
- enriched contacts
- stages
- relations
- governance
- shareholding
    """,
    "category": "CRM",
    "author": "Sydel",
    "website": "https://www.sydel.fr",
    "license": "LGPL-3",
    "depends": [
        "contacts",
        "mail",
    ],
    "data": [
        "security/sydel_contact_groups.xml",
        "security/ir.model.access.csv",
        "data/sydel_contact_stage_data.xml",
        "data/sydel_contact_relation_type_data.xml",
        "data/sydel_legal_form_data.xml",
        "views/res_partner_views.xml",
        "views/sydel_contact_stage_views.xml",
        "views/sydel_contact_relation_views.xml",
        "views/sydel_contact_relation_type_views.xml",
        "views/sydel_contact_shareholding_views.xml",
        "views/sydel_contact_management_views.xml",
        "views/sydel_legal_form_views.xml",
        "views/sydel_contact_menus.xml",
    ],
    "installable": True,
    "application": False,
}
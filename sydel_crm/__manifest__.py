{
    'name': 'Sydel CRM',
    'version': '19.0.1.0.1',
    'category': 'Sales/CRM',
    'summary': 'Module CRM custom pour le cabinet Sydel',
    'description': """
        Module CRM développé sur mesure pour le cabinet Sydel.

        Fonctionnalités :
        - Gestion de contacts personnes physiques et morales
        - Champs métier spécifiques (RPPS, SIREN, SIRET, régime matrimonial...)
        - Répartition du capital social et dirigeants
        - Toile des liens professionnels entre contacts
        - Gestion documentaire par contact
        - Pipeline CRM personnalisé (appel découverte → lettre de mission)
        - Attribution multi-utilisateurs et filtre "Mes contacts"
    """,
    'author': 'Sydel',
    'website': 'https://www.sydel.fr',
    'license': 'LGPL-3',
    'depends': [
        'crm',
        'contacts',
        'mail',
    ],
    'data': [
        # Sécurité — toujours en premier
        'security/security.xml',
        'security/ir.model.access.csv',
        # Données initiales
        'data/crm_stage_data.xml',
        'data/partner_category_data.xml',
        'data/relation_type_data.xml',
        # Vues — modèles de base d'abord, puis les héritages
        'views/sydel_relation_type_views.xml',
        'views/sydel_capital_share_views.xml',
        'views/sydel_company_director_views.xml',
        'views/sydel_contact_relation_views.xml',
        'views/sydel_contact_document_views.xml',
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
        'views/menuitems.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

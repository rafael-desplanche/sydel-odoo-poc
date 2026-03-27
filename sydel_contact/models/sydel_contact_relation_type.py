from odoo import fields, models


class SydelContactRelationType(models.Model):
    _name = "sydel.contact.relation.type"
    _description = "Sydel Contact Relation Type"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(help="Short technical code for integrations.")
    active = fields.Boolean(default=True)
    description = fields.Text()

    _sql_constraints = [
        ("sydel_contact_relation_type_code_uniq", "unique(code)", "Relation type code must be unique."),
    ]

from odoo import fields, models


class SydelLegalForm(models.Model):
    _name = "sydel.legal.form"
    _description = "Sydel Legal Form"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
    note = fields.Text()

    _sql_constraints = [
        ("sydel_legal_form_code_uniq", "unique(code)", "Legal form code must be unique."),
    ]

from odoo import fields, models


class SydelContactStage(models.Model):
    _name = "sydel.contact.stage"
    _description = "Sydel Contact Stage"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    fold = fields.Boolean(string="Folded in Pipeline")
    description = fields.Text()

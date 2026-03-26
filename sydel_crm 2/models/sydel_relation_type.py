from odoo import fields, models


class SydelRelationType(models.Model):
    _name = 'sydel.relation.type'
    _description = "Type de relation entre contacts"
    _order = 'name'

    active = fields.Boolean(
        default=True,
    )
    name = fields.Char(
        string="Nom du type",
        required=True,
    )
    forward_label = fields.Char(
        string="Libellé aller",
        required=True,
        help="Ex: 'emploie', 'dirige', 'est associé(e) de'",
    )
    reverse_label = fields.Char(
        string="Libellé retour",
        required=True,
        help="Ex: 'est employé(e) par', 'est dirigée par'",
    )

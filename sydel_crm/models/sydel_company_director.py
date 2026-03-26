from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SydelCompanyDirector(models.Model):
    _name = 'sydel.company.director'
    _description = "Dirigeant de société"
    _order = 'start_date desc'
    _rec_name = 'director_id'

    active = fields.Boolean(
        default=True,
    )
    company_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Société",
        required=True,
        ondelete='cascade',
        domain="[('is_company', '=', True)]",
    )
    director_id = fields.Many2one(
        comodel_name='res.partner',
        string="Dirigeant",
        required=True,
        ondelete='restrict',
    )
    role = fields.Selection(
        selection=[
            ('president', "Président"),
            ('dg', "Directeur général"),
            ('gerant', "Gérant"),
            ('administrateur', "Administrateur"),
            ('other', "Autre"),
        ],
        string="Fonction",
    )
    role_other = fields.Char(
        string="Fonction (autre)",
    )
    start_date = fields.Date(
        string="Début de mandat",
    )
    end_date = fields.Date(
        string="Fin de mandat",
    )

    # -------------------------------------------------------------------------
    # Contraintes
    # -------------------------------------------------------------------------
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for director in self:
            if director.start_date and director.end_date:
                if director.end_date < director.start_date:
                    raise ValidationError(
                        _("La date de fin de mandat ne peut pas être antérieure à la date de début.")
                    )

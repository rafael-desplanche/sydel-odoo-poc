from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SydelCapitalShare(models.Model):
    _name = 'sydel.capital.share'
    _description = "Répartition du capital social"
    _order = 'share_percentage desc'
    _rec_name = 'shareholder_id'

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
    shareholder_id = fields.Many2one(
        comodel_name='res.partner',
        string="Associé / Actionnaire",
        required=True,
        ondelete='restrict',
    )
    share_percentage = fields.Float(
        string="Part (%)",
        digits=(5, 2),
        required=True,
    )
    share_count = fields.Integer(
        string="Nombre de parts",
    )
    share_amount = fields.Monetary(
        string="Montant",
        compute='_compute_share_amount',
        store=True,
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_partner_id.currency_id',
    )

    # -------------------------------------------------------------------------
    # Compute
    # -------------------------------------------------------------------------
    @api.depends('share_percentage', 'company_partner_id.share_capital')
    def _compute_share_amount(self):
        for line in self:
            if line.share_percentage and line.company_partner_id.share_capital:
                line.share_amount = (
                    line.share_percentage / 100.0
                ) * line.company_partner_id.share_capital
            else:
                line.share_amount = 0.0

    # -------------------------------------------------------------------------
    # Contraintes
    # -------------------------------------------------------------------------
    @api.constrains('share_percentage')
    def _check_percentage(self):
        for line in self:
            if line.share_percentage <= 0 or line.share_percentage > 100:
                raise ValidationError(
                    _("Le pourcentage de participation doit être compris entre 0 et 100.")
                )

    @api.constrains('share_percentage', 'company_partner_id')
    def _check_total_percentage(self):
        for line in self:
            if not line.company_partner_id:
                continue
            total = sum(
                line.company_partner_id.capital_share_ids
                .filtered(lambda l: l.active)
                .mapped('share_percentage')
            )
            if total > 100:
                raise ValidationError(
                    _("La somme des participations ne peut pas dépasser 100%%. "
                      "Total actuel : %(total).2f%%",
                      total=total)
                )

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SydelContactShareholding(models.Model):
    _name = "sydel.contact.shareholding"
    _description = "Sydel Contact Shareholding"
    _order = "company_partner_id, percentage desc, id desc"

    name = fields.Char(compute="_compute_name", store=True)
    company_partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade", index=True)
    shareholder_partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade", index=True)
    percentage = fields.Float(digits=(5, 2), help="Shareholding percentage from 0 to 100.")
    shares_number = fields.Integer()
    note = fields.Text()
    active = fields.Boolean(default=True)

    @api.depends("company_partner_id", "shareholder_partner_id", "percentage")
    def _compute_name(self):
        for rec in self:
            company = rec.company_partner_id.display_name or ""
            holder = rec.shareholder_partner_id.display_name or ""
            pct = f"{rec.percentage:.2f}%" if rec.percentage else "0.00%"
            rec.name = f"{holder} -> {company} ({pct})" if company and holder else company or holder

    @api.constrains("company_partner_id", "shareholder_partner_id")
    def _check_not_self(self):
        for rec in self:
            if rec.company_partner_id and rec.company_partner_id == rec.shareholder_partner_id:
                raise ValidationError("A partner cannot be shareholder of itself.")

    @api.constrains("percentage")
    def _check_percentage(self):
        for rec in self:
            if rec.percentage < 0 or rec.percentage > 100:
                raise ValidationError("Shareholding percentage must be between 0 and 100.")

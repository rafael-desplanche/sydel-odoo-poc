from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SydelContactManagement(models.Model):
    _name = "sydel.contact.management"
    _description = "Sydel Contact Management"
    _order = "start_date desc, id desc"

    name = fields.Char(compute="_compute_name", store=True)
    partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade", index=True)
    manager_partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade", index=True)
    role = fields.Char(required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    is_active = fields.Boolean(default=True)
    note = fields.Text()

    @api.depends("partner_id", "manager_partner_id", "role")
    def _compute_name(self):
        for rec in self:
            company = rec.partner_id.display_name or ""
            manager = rec.manager_partner_id.display_name or ""
            role = rec.role or ""
            rec.name = " - ".join([part for part in [company, role, manager] if part])

    @api.constrains("partner_id", "manager_partner_id")
    def _check_not_same_partner(self):
        for rec in self:
            if rec.partner_id and rec.partner_id == rec.manager_partner_id:
                raise ValidationError("A manager link must target a different partner.")

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError("Management end date must be greater than or equal to start date.")

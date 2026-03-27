from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SydelContactRelation(models.Model):
    _name = "sydel.contact.relation"
    _description = "Sydel Contact Relation"
    _order = "start_date desc, id desc"

    name = fields.Char(compute="_compute_name", store=True)
    left_partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade", index=True)
    right_partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade", index=True)
    relation_type_id = fields.Many2one("sydel.contact.relation.type", required=True, ondelete="restrict")
    start_date = fields.Date()
    end_date = fields.Date()
    note = fields.Text()
    active = fields.Boolean(default=True)

    @api.depends("left_partner_id", "relation_type_id", "right_partner_id")
    def _compute_name(self):
        for rec in self:
            left = rec.left_partner_id.display_name or ""
            rel = rec.relation_type_id.name or ""
            right = rec.right_partner_id.display_name or ""
            rec.name = " / ".join([part for part in [left, rel, right] if part])

    @api.constrains("left_partner_id", "right_partner_id")
    def _check_not_same_partner(self):
        for rec in self:
            if rec.left_partner_id and rec.left_partner_id == rec.right_partner_id:
                raise ValidationError("A relation cannot link the same partner on both sides.")

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError("Relation end date must be greater than or equal to start date.")

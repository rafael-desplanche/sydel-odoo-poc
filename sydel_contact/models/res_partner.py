import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    sydel_firstname = fields.Char(string="First Name")
    sydel_lastname = fields.Char(string="Last Name")

    sydel_stage_id = fields.Many2one("sydel.contact.stage", string="Stage", tracking=True)
    sydel_user_ids = fields.Many2many(
        "res.users",
        "res_partner_sydel_user_rel",
        "partner_id",
        "user_id",
        string="Assigned Users",
    )
    sydel_internal_note = fields.Text(string="Internal Note")

    sydel_is_natural_person = fields.Boolean(string="Natural Person", compute="_compute_person_flags", store=True)
    sydel_is_legal_entity = fields.Boolean(string="Legal Entity", compute="_compute_person_flags", store=True)

    sydel_birthdate = fields.Date(string="Birthdate")
    sydel_nationality = fields.Char(string="Nationality")
    sydel_id_number = fields.Char(string="Identity Number")

    sydel_legal_form_id = fields.Many2one("sydel.legal.form", string="Legal Form")
    sydel_siren = fields.Char(string="SIREN")
    sydel_registration_city = fields.Char(string="Registration City")

    sydel_currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    sydel_capital_amount = fields.Monetary(string="Share Capital", currency_field="sydel_currency_id")

    sydel_governance_note = fields.Text(string="Governance")

    sydel_relation_left_ids = fields.One2many(
        "sydel.contact.relation", "left_partner_id", string="Relations (Source)"
    )
    sydel_relation_right_ids = fields.One2many(
        "sydel.contact.relation", "right_partner_id", string="Relations (Target)"
    )
    sydel_shareholding_company_ids = fields.One2many(
        "sydel.contact.shareholding", "company_partner_id", string="Shareholdings (Company)"
    )
    sydel_shareholding_holder_ids = fields.One2many(
        "sydel.contact.shareholding", "shareholder_partner_id", string="Shareholdings (Shareholder)"
    )
    sydel_management_ids = fields.One2many("sydel.contact.management", "partner_id", string="Governance Roles")

    sydel_relation_count = fields.Integer(compute="_compute_sydel_counts")
    sydel_shareholding_count = fields.Integer(compute="_compute_sydel_counts")
    sydel_management_count = fields.Integer(compute="_compute_sydel_counts")

    @api.depends("company_type")
    def _compute_person_flags(self):
        for rec in self:
            rec.sydel_is_natural_person = rec.company_type == "person"
            rec.sydel_is_legal_entity = rec.company_type == "company"

    @api.depends(
        "sydel_relation_left_ids",
        "sydel_relation_right_ids",
        "sydel_shareholding_company_ids",
        "sydel_shareholding_holder_ids",
        "sydel_management_ids",
    )
    def _compute_sydel_counts(self):
        for rec in self:
            rec.sydel_relation_count = len(rec.sydel_relation_left_ids) + len(rec.sydel_relation_right_ids)
            rec.sydel_shareholding_count = len(rec.sydel_shareholding_company_ids) + len(
                rec.sydel_shareholding_holder_ids
            )
            rec.sydel_management_count = len(rec.sydel_management_ids)

    @api.model_create_multi
    def create(self, vals_list):
        self._sync_person_name_vals(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        vals = dict(vals)
        self._sync_person_name_vals([vals], records=self)
        return super().write(vals)

    def _sync_person_name_vals(self, vals_list, records=None):
        for index, vals in enumerate(vals_list):
            company_type = vals.get("company_type")
            if company_type is None and records and len(records) == len(vals_list):
                company_type = records[index].company_type

            first_name = vals.get("sydel_firstname")
            last_name = vals.get("sydel_lastname")
            if records and len(records) == len(vals_list):
                if first_name is None:
                    first_name = records[index].sydel_firstname
                if last_name is None:
                    last_name = records[index].sydel_lastname

            if company_type == "person" and (first_name or last_name):
                vals["name"] = " ".join([part for part in [first_name, last_name] if part]).strip()

    @api.constrains("sydel_siren", "company_type")
    def _check_siren(self):
        siren_regex = re.compile(r"^\d{9}$")
        for rec in self:
            if rec.company_type == "company" and rec.sydel_siren and not siren_regex.match(rec.sydel_siren):
                raise ValidationError("SIREN must contain exactly 9 digits.")

    def action_view_sydel_relations(self):
        self.ensure_one()
        action = self.env.ref("sydel_contact.action_sydel_contact_relation").read()[0]
        action["domain"] = ["|", ("left_partner_id", "=", self.id), ("right_partner_id", "=", self.id)]
        action["context"] = {
            "default_left_partner_id": self.id,
            "default_right_partner_id": self.id,
        }
        return action

    def action_view_sydel_shareholdings(self):
        self.ensure_one()
        action = self.env.ref("sydel_contact.action_sydel_contact_shareholding").read()[0]
        action["domain"] = [
            "|",
            ("company_partner_id", "=", self.id),
            ("shareholder_partner_id", "=", self.id),
        ]
        action["context"] = {
            "default_company_partner_id": self.id,
            "default_shareholder_partner_id": self.id,
        }
        return action

    def action_view_sydel_management(self):
        self.ensure_one()
        action = self.env.ref("sydel_contact.action_sydel_contact_management").read()[0]
        action["domain"] = [("partner_id", "=", self.id)]
        action["context"] = {"default_partner_id": self.id}
        return action

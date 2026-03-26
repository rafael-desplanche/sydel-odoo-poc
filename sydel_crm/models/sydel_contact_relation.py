from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SydelContactRelation(models.Model):
    _name = 'sydel.contact.relation'
    _description = "Relation entre contacts"
    _order = 'start_date desc, id desc'

    active = fields.Boolean(
        default=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Contact",
        required=True,
        ondelete='cascade',
    )
    related_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Contact lié",
        required=True,
        ondelete='cascade',
    )
    relation_type_id = fields.Many2one(
        comodel_name='sydel.relation.type',
        string="Type de relation",
        required=True,
        ondelete='restrict',
    )
    start_date = fields.Date(
        string="Début",
    )
    end_date = fields.Date(
        string="Fin",
    )
    notes = fields.Text(
        string="Notes",
    )

    # -------------------------------------------------------------------------
    # Contraintes SQL
    # -------------------------------------------------------------------------
    _sql_constraints = [
        (
            'unique_relation',
            'UNIQUE(partner_id, related_partner_id, relation_type_id)',
            "Cette relation existe déjà entre ces deux contacts.",
        ),
    ]

    # -------------------------------------------------------------------------
    # Contraintes Python
    # -------------------------------------------------------------------------
    @api.constrains('partner_id', 'related_partner_id')
    def _check_no_self_relation(self):
        for relation in self:
            if relation.partner_id == relation.related_partner_id:
                raise ValidationError(
                    _("Un contact ne peut pas avoir une relation avec lui-même.")
                )

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for relation in self:
            if relation.start_date and relation.end_date:
                if relation.end_date < relation.start_date:
                    raise ValidationError(
                        _("La date de fin ne peut pas être antérieure à la date de début.")
                    )

    # -------------------------------------------------------------------------
    # CRUD — Logique de relation miroir
    # -------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get('skip_mirror'):
            self._create_mirror_relations(records)
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'active' in vals and not self.env.context.get('skip_mirror'):
            self._sync_mirror_active(vals['active'])
        return res

    def unlink(self):
        if not self.env.context.get('skip_mirror'):
            mirrors = self._find_mirror_relations()
            if mirrors:
                mirrors.with_context(skip_mirror=True).unlink()
        return super().unlink()

    # -------------------------------------------------------------------------
    # Méthodes privées — Gestion du miroir
    # -------------------------------------------------------------------------
    def _create_mirror_relations(self, records):
        """Crée la relation inverse pour chaque relation créée."""
        inverse_vals = []
        for rec in records:
            existing = self.search([
                ('partner_id', '=', rec.related_partner_id.id),
                ('related_partner_id', '=', rec.partner_id.id),
                ('relation_type_id', '=', rec.relation_type_id.id),
            ], limit=1)
            if not existing:
                inverse_vals.append({
                    'partner_id': rec.related_partner_id.id,
                    'related_partner_id': rec.partner_id.id,
                    'relation_type_id': rec.relation_type_id.id,
                    'start_date': rec.start_date,
                    'end_date': rec.end_date,
                    'notes': rec.notes,
                })
        if inverse_vals:
            self.with_context(skip_mirror=True).create(inverse_vals)

    def _find_mirror_relations(self):
        """Trouve les relations miroir correspondantes."""
        mirrors = self.env['sydel.contact.relation']
        for rec in self:
            mirror = self.search([
                ('partner_id', '=', rec.related_partner_id.id),
                ('related_partner_id', '=', rec.partner_id.id),
                ('relation_type_id', '=', rec.relation_type_id.id),
            ], limit=1)
            mirrors |= mirror
        return mirrors

    def _sync_mirror_active(self, active_value):
        """Synchronise l'état actif/archivé avec les relations miroir."""
        mirrors = self._find_mirror_relations()
        if mirrors:
            mirrors.with_context(skip_mirror=True).write({'active': active_value})

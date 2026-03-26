from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestContactRelation(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_a = cls.env['res.partner'].create({
            'name': 'Alice', 'is_company': False,
        })
        cls.partner_b = cls.env['res.partner'].create({
            'name': 'Bob', 'is_company': False,
        })
        cls.relation_type = cls.env['sydel.relation.type'].create({
            'name': 'Emploi',
            'forward_label': 'emploie',
            'reverse_label': 'est employé(e) par',
        })

    # -----------------------------------------------------------------
    # Création miroir
    # -----------------------------------------------------------------
    def test_mirror_created_on_create(self):
        """Créer A→B doit aussi créer B→A."""
        self.env['sydel.contact.relation'].create({
            'partner_id': self.partner_a.id,
            'related_partner_id': self.partner_b.id,
            'relation_type_id': self.relation_type.id,
        })
        mirror = self.env['sydel.contact.relation'].search([
            ('partner_id', '=', self.partner_b.id),
            ('related_partner_id', '=', self.partner_a.id),
            ('relation_type_id', '=', self.relation_type.id),
        ])
        self.assertEqual(len(mirror), 1)

    def test_no_duplicate_mirror(self):
        """Créer A→B ne doit pas créer un doublon si B→A existe déjà."""
        self.env['sydel.contact.relation'].create({
            'partner_id': self.partner_a.id,
            'related_partner_id': self.partner_b.id,
            'relation_type_id': self.relation_type.id,
        })
        total = self.env['sydel.contact.relation'].search_count([
            ('relation_type_id', '=', self.relation_type.id),
            '|',
            '&', ('partner_id', '=', self.partner_a.id),
                 ('related_partner_id', '=', self.partner_b.id),
            '&', ('partner_id', '=', self.partner_b.id),
                 ('related_partner_id', '=', self.partner_a.id),
        ])
        self.assertEqual(total, 2)

    # -----------------------------------------------------------------
    # Suppression miroir
    # -----------------------------------------------------------------
    def test_mirror_deleted_on_unlink(self):
        """Supprimer A→B doit aussi supprimer B→A."""
        relation = self.env['sydel.contact.relation'].create({
            'partner_id': self.partner_a.id,
            'related_partner_id': self.partner_b.id,
            'relation_type_id': self.relation_type.id,
        })
        relation.unlink()
        remaining = self.env['sydel.contact.relation'].search([
            ('partner_id', '=', self.partner_b.id),
            ('related_partner_id', '=', self.partner_a.id),
            ('relation_type_id', '=', self.relation_type.id),
        ])
        self.assertEqual(len(remaining), 0)

    # -----------------------------------------------------------------
    # Archivage miroir
    # -----------------------------------------------------------------
    def test_mirror_archived_on_archive(self):
        """Archiver A→B doit aussi archiver B→A."""
        relation = self.env['sydel.contact.relation'].create({
            'partner_id': self.partner_a.id,
            'related_partner_id': self.partner_b.id,
            'relation_type_id': self.relation_type.id,
        })
        relation.write({'active': False})
        mirror = self.env['sydel.contact.relation'].with_context(
            active_test=False
        ).search([
            ('partner_id', '=', self.partner_b.id),
            ('related_partner_id', '=', self.partner_a.id),
            ('relation_type_id', '=', self.relation_type.id),
        ])
        self.assertFalse(mirror.active)

    # -----------------------------------------------------------------
    # Auto-relation interdite
    # -----------------------------------------------------------------
    def test_self_relation_forbidden(self):
        with self.assertRaises(ValidationError):
            self.env['sydel.contact.relation'].create({
                'partner_id': self.partner_a.id,
                'related_partner_id': self.partner_a.id,
                'relation_type_id': self.relation_type.id,
            })

    # -----------------------------------------------------------------
    # Dates incohérentes
    # -----------------------------------------------------------------
    def test_end_date_before_start_date(self):
        with self.assertRaises(ValidationError):
            self.env['sydel.contact.relation'].create({
                'partner_id': self.partner_a.id,
                'related_partner_id': self.partner_b.id,
                'relation_type_id': self.relation_type.id,
                'start_date': '2025-06-01',
                'end_date': '2025-01-01',
            })

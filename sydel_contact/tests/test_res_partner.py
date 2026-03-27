from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestResPartnerSydel(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Stage = cls.env["sydel.contact.stage"]
        cls.Partner = cls.env["res.partner"]
        cls.RelationType = cls.env["sydel.contact.relation.type"]
        cls.Relation = cls.env["sydel.contact.relation"]

        cls.stage = cls.Stage.search([], limit=1)
        cls.relation_type = cls.RelationType.search([], limit=1)

    def test_create_person_syncs_name(self):
        partner = self.Partner.create(
            {
                "company_type": "person",
                "sydel_firstname": "Gad",
                "sydel_lastname": "Tibi",
                "sydel_stage_id": self.stage.id,
            }
        )
        self.assertEqual(partner.name, "Gad Tibi")

    def test_siren_constraint(self):
        with self.assertRaises(ValidationError):
            self.Partner.create(
                {
                    "name": "Bad Company",
                    "company_type": "company",
                    "sydel_siren": "123",
                }
            )

    def test_relation_cannot_link_same_partner(self):
        partner = self.Partner.create(
            {
                "name": "Test Company",
                "company_type": "company",
            }
        )
        with self.assertRaises(ValidationError):
            self.Relation.create(
                {
                    "left_partner_id": partner.id,
                    "right_partner_id": partner.id,
                    "relation_type_id": self.relation_type.id,
                }
            )
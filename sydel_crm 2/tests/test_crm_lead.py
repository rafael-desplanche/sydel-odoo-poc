from odoo.tests.common import TransactionCase


class TestCrmLead(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Client Test',
            'is_company': False,
        })

    # -----------------------------------------------------------------
    # Création d'opportunité avec champs custom
    # -----------------------------------------------------------------
    def test_create_lead_with_mission_type(self):
        lead = self.env['crm.lead'].create({
            'name': 'Mission conseil fiscal',
            'partner_id': self.partner.id,
            'type': 'opportunity',
            'mission_type': 'tax',
            'next_action_date': '2026-04-01',
            'next_action_note': 'Relancer par téléphone',
        })
        self.assertEqual(lead.mission_type, 'tax')
        self.assertEqual(str(lead.next_action_date), '2026-04-01')

    def test_create_lead_with_letter_dates(self):
        lead = self.env['crm.lead'].create({
            'name': 'Mission comptabilité',
            'partner_id': self.partner.id,
            'type': 'opportunity',
            'mission_type': 'accounting',
            'mission_letter_sent_date': '2026-03-15',
            'mission_letter_signed_date': '2026-03-20',
        })
        self.assertTrue(lead.mission_letter_signed_date > lead.mission_letter_sent_date)

    # -----------------------------------------------------------------
    # Vérification des stages initiaux
    # -----------------------------------------------------------------
    def test_pipeline_stages_exist(self):
        """Les 6 stages du pipeline Sydel doivent exister après installation."""
        stages = self.env['crm.stage'].search([])
        stage_names = stages.mapped('name')
        self.assertIn('Appel de découverte', stage_names)
        self.assertIn('R1 — Premier rendez-vous', stage_names)
        self.assertIn('R2 — Deuxième rendez-vous', stage_names)
        self.assertIn('Lettre de mission envoyée', stage_names)
        self.assertIn('Lettre de mission signée', stage_names)
        self.assertIn('Lettre de mission non signée', stage_names)

    def test_stage_signed_is_won(self):
        """Le stage 'Lettre de mission signée' doit être marqué is_won."""
        stage = self.env.ref('sydel_crm.stage_letter_signed')
        self.assertTrue(stage.is_won)

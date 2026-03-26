from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCapitalShare(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.partner'].create({
            'name': 'SCI Test',
            'is_company': True,
            'share_capital': 100000,
            'total_shares': 1000,
        })
        cls.partner_a = cls.env['res.partner'].create({
            'name': 'Associé A',
            'is_company': False,
        })
        cls.partner_b = cls.env['res.partner'].create({
            'name': 'Associé B',
            'is_company': False,
        })

    # -----------------------------------------------------------------
    # Création valide
    # -----------------------------------------------------------------
    def test_create_share_line(self):
        line = self.env['sydel.capital.share'].create({
            'company_partner_id': self.company.id,
            'shareholder_id': self.partner_a.id,
            'share_percentage': 60.0,
            'share_count': 600,
        })
        self.assertEqual(line.share_amount, 60000.0)

    # -----------------------------------------------------------------
    # Pourcentage invalide
    # -----------------------------------------------------------------
    def test_percentage_over_100(self):
        with self.assertRaises(ValidationError):
            self.env['sydel.capital.share'].create({
                'company_partner_id': self.company.id,
                'shareholder_id': self.partner_a.id,
                'share_percentage': 150.0,
            })

    def test_percentage_zero(self):
        with self.assertRaises(ValidationError):
            self.env['sydel.capital.share'].create({
                'company_partner_id': self.company.id,
                'shareholder_id': self.partner_a.id,
                'share_percentage': 0.0,
            })

    # -----------------------------------------------------------------
    # Somme des parts > 100%
    # -----------------------------------------------------------------
    def test_total_percentage_over_100(self):
        self.env['sydel.capital.share'].create({
            'company_partner_id': self.company.id,
            'shareholder_id': self.partner_a.id,
            'share_percentage': 70.0,
        })
        with self.assertRaises(ValidationError):
            self.env['sydel.capital.share'].create({
                'company_partner_id': self.company.id,
                'shareholder_id': self.partner_b.id,
                'share_percentage': 40.0,
            })

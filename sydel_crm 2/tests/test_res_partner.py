from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_physical = cls.env['res.partner'].create({
            'name': 'Dupont',
            'firstname': 'Marie',
            'is_company': False,
        })
        cls.partner_company = cls.env['res.partner'].create({
            'name': 'SCI Flore',
            'is_company': True,
        })

    # -----------------------------------------------------------------
    # Compute — Âge
    # -----------------------------------------------------------------
    def test_age_computed_from_birthdate(self):
        self.partner_physical.birthdate = date.today() - relativedelta(years=32)
        self.assertEqual(self.partner_physical.age, 32)

    def test_age_zero_when_no_birthdate(self):
        self.partner_physical.birthdate = False
        self.assertEqual(self.partner_physical.age, 0)

    # -----------------------------------------------------------------
    # Compute — Valeur de la part
    # -----------------------------------------------------------------
    def test_share_value_computed(self):
        self.partner_company.write({
            'share_capital': 50000,
            'total_shares': 1000,
        })
        self.assertEqual(self.partner_company.share_value, 50.0)

    def test_share_value_zero_when_no_shares(self):
        self.partner_company.write({
            'share_capital': 50000,
            'total_shares': 0,
        })
        self.assertEqual(self.partner_company.share_value, 0.0)

    # -----------------------------------------------------------------
    # Contrainte — RPPS
    # -----------------------------------------------------------------
    def test_rpps_valid(self):
        self.partner_physical.rpps_number = '12345678901'

    def test_rpps_invalid_too_short(self):
        with self.assertRaises(ValidationError):
            self.partner_physical.rpps_number = '12345'

    def test_rpps_invalid_letters(self):
        with self.assertRaises(ValidationError):
            self.partner_physical.rpps_number = '1234567890A'

    # -----------------------------------------------------------------
    # Contrainte — SIREN
    # -----------------------------------------------------------------
    def test_siren_valid(self):
        self.partner_company.siren = '823456789'

    def test_siren_invalid(self):
        with self.assertRaises(ValidationError):
            self.partner_company.siren = '82345'

    # -----------------------------------------------------------------
    # Contrainte — SIRET
    # -----------------------------------------------------------------
    def test_siret_valid(self):
        self.partner_company.write({
            'siren': '823456789',
            'siret': '82345678900012',
        })

    def test_siret_invalid_format(self):
        with self.assertRaises(ValidationError):
            self.partner_company.siret = '1234'

    # -----------------------------------------------------------------
    # Contrainte — Cohérence SIREN/SIRET
    # -----------------------------------------------------------------
    def test_siren_siret_mismatch(self):
        with self.assertRaises(ValidationError):
            self.partner_company.write({
                'siren': '823456789',
                'siret': '99999999900012',
            })

    # -----------------------------------------------------------------
    # Contrainte — NAF
    # -----------------------------------------------------------------
    def test_naf_valid(self):
        self.partner_company.naf_code = '6920Z'

    def test_naf_invalid(self):
        with self.assertRaises(ValidationError):
            self.partner_company.naf_code = 'ABCDE'

    # -----------------------------------------------------------------
    # Contrainte — N° ordre
    # -----------------------------------------------------------------
    def test_ordre_valid(self):
        self.partner_physical.ordre_number = '123456789'

    def test_ordre_invalid(self):
        with self.assertRaises(ValidationError):
            self.partner_physical.ordre_number = '12345'

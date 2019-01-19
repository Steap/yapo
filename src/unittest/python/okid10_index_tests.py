import unittest

import pandas as pd
import numpy as np

import yapo
from yapo._settings import _MONTHS_PER_YEAR


class Okid10IndexTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.asset_name = 'index/OKID10'
        cls.places = 4

    def test__present_in_available_names(self):
        sym_ids = {x.fin_sym_id.format() for x in yapo.available_names(namespace='index')}
        self.assertTrue(self.asset_name in sym_ids)

    def test__have_valid_max_period_range(self):
        okid10 = yapo.portfolio_asset(name=self.asset_name)
        cbr_top10 = yapo.portfolio_asset(name='cbr/TOP_rates')

        self.assertEqual(okid10.period_min, cbr_top10.period_min + _MONTHS_PER_YEAR)
        self.assertEqual(okid10.period_max, cbr_top10.period_max)

    def test__have_valid_selected_period_range(self):
        start_period = pd.Period('2013-1', freq='M')
        end_period = pd.Period('2015-3', freq='M')

        okid10 = yapo.portfolio_asset(name=self.asset_name, start_period=str(start_period), end_period=str(end_period))
        self.assertEqual(okid10.period_min, start_period)
        self.assertEqual(okid10.period_max, end_period)

    def test__have_correct_values(self):
        okid10 = yapo.portfolio_asset(name=self.asset_name, end_period='2018-12')
        np.testing.assert_almost_equal(okid10.values[:5].values,
                                       [1290.8230, 1303.5421, 1315.8087, 1327.6302, 1339.0072], decimal=self.places)
        np.testing.assert_almost_equal(okid10.values[-5:].values,
                                       [2737.4407, 2752.9855, 2768.5141, 2784.0878, 2799.7449], decimal=self.places)

    def test__compute_correctly_in_other_currencies(self):
        okid10_usd = yapo.portfolio_asset(name=self.asset_name, end_period='2018-12', currency='usd')
        okid10_rub = yapo.portfolio_asset(name=self.asset_name, end_period='2018-12', currency='rub')

        okid10_currency_rate = okid10_usd.close() / okid10_rub.close()

        vs_rub = yapo.portfolio_asset(name='cbr/RUB',
                                      start_period=okid10_currency_rate.start_period,
                                      end_period=okid10_currency_rate.end_period,
                                      currency='usd').close()

        np.testing.assert_almost_equal(okid10_currency_rate.values, vs_rub.values, decimal=self.places)
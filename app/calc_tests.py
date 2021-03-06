from calc import CalcCapRate
import unittest
from copy import deepcopy


class CalcTestCase(unittest.TestCase):

    def setUp(self):
        self.test1_input = {'cash_on_cash': 10,
                            'target_ltv': 80,
                            'mezz_debt': 0,
                            'transfer_cost': 2,
                            'transfer_buyer_share': 50,
                            'recordation_cost': 5,
                            'recordation_buyer_share': 50,
                            'finance': 1,
                            'interest': 6,
                            'amort': 30,
                            'mezz_rate': 8,
                            'mezz_interest_only': True,
                            'mezz_secured': False,
                            'mezz_amort': 30,
                            'income_appr': 0,
                            'apprec_depr': 0,
                            'holding_period': 5}

        self.test1_output = {'first_mort': 0.0564,
                             'mezz': 0.000,
                             'calc_yield': 0.0298,
                             'amort_first_mort': -0.0083,
                             'amort_mezz': 0.000,
                             'appr': 0.000,
                             'cap_rate': 0.078,
                             'sinking_fund_factor': .1518,
                             'appr_depr_factor': 0.000,
                             'op_cap_rate': 0.07955}

        # Same as test1 but cash_on_cash is 20%
        self.test2_input = deepcopy(self.test1_input)
        self.test2_input['cash_on_cash'] = 20
        self.test2_output = {'first_mort': 0.056428,
                             'mezz': 0.000,
                             'calc_yield': 0.050019,
                             'amort_first_mort': -0.006876,
                             'amort_mezz': 0.000,
                             'appr': 0.000,
                             'cap_rate': 0.099571,
                             'sinking_fund_factor': .1262,
                             'appr_depr_factor': 0.000,
                             'op_cap_rate': 0.1015}

        # Same as test1 but mezz_debt is 5%
        self.test3_input = deepcopy(self.test1_input)
        self.test3_input['mezz_debt'] = 5
        self.test3_output = {'first_mort': 0.056428,
                             'mezz': 0.004,
                             'calc_yield': 0.024668,
                             'amort_first_mort': -0.008097,
                             'amort_mezz': 0.000,
                             'appr': 0.000,
                             'cap_rate': 0.076999,
                             'sinking_fund_factor': .1486,
                             'appr_depr_factor': 0.000,
                             'op_cap_rate': 0.0786}

        # Test including appreciation
        self.test4_input = {'cash_on_cash': 10,
                            'target_ltv': 80,
                            'mezz_debt': 0,
                            'transfer_cost': 2,
                            'transfer_buyer_share': 50,
                            'recordation_cost': 5,
                            'recordation_buyer_share': 50,
                            'finance': 1,
                            'interest': 4.75,
                            'amort': 30,
                            'mezz_rate': 0,
                            'mezz_interest_only': True,
                            'mezz_secured': False,
                            'mezz_amort': 30,
                            'apprec_depr': 5,
                            'income_appr': 0,
                            'holding_period': 7}

        self.test4_output = {'first_mort': 0.0491,
                             'mezz': 0.000,
                             'calc_yield': 0.034570,
                             'amort_first_mort': -0.0086,
                             'amort_mezz': 0.000,
                             'appr': -0.0044,
                             'cap_rate': 0.0707,
                             'sinking_fund_factor': .08757,
                             'appr_depr_factor': -0.004389,
                             'op_cap_rate': 0.0721}

        # Base J Factor test
        self.jfactor1_input = deepcopy(self.test1_input)
        self.jfactor1_input['income_appr'] = 0
        self.jfactor1_output = deepcopy(self.test1_output)
        self.jfactor1_output['j_factor'] = 0.49441

        # J Factor with income appreciation
        self.jfactor2_input = deepcopy(self.jfactor1_input)
        self.jfactor2_input['income_appr'] = 10
        self.jfactor2_output = deepcopy(self.jfactor1_output)
        self.jfactor2_output['first_mort'] = 0.0538
        self.jfactor2_output['calc_yield'] = 0.0284
        self.jfactor2_output['amort_first_mort'] = -0.0079
        self.jfactor2_output['cap_rate'] = 0.07431
        self.jfactor2_output['op_cap_rate'] = 0.07579

        # Test including cash flow
        self.cash_flow_input = {'cash_on_cash': 8,
                                'target_ltv': 70,
                                'mezz_debt': 10,
                                'transfer_cost': 2,
                                'transfer_buyer_share': 50,
                                'recordation_cost': 5,
                                'recordation_buyer_share': 50,
                                'finance': 1,
                                'interest': 5,
                                'amort': 30,
                                'mezz_rate': 5,
                                'mezz_interest_only': False,
                                'mezz_secured': True,
                                'mezz_amort': 30,
                                'apprec_depr': 5,
                                'income_appr': 5,
                                'holding_period': 5}

        self.cash_flow_output = {'first_mort': 0.0432,
                                 'mezz': 0.0063,
                                 'base_cash_flow': 0.0327,
                                 'cash_flow_growth': 0.0016,
                                 'calc_yield': -0.0070,
                                 'amort_first_mort': -0.0079,
                                 'amort_mezz': -0.0011,
                                 'appr': -0.0070,
                                 'cap_rate': 0.0677,
                                 'sinking_fund_factor': .144008,
                                 'appr_depr_factor': -0.0072004,
                                 'op_cap_rate': 0.0691}

    def test_init_scenario_1(self):
        c = CalcCapRate(self.test1_input)
        self.assertEqual(c.cash_on_cash, 0.10)
        self.assertEqual(c.interest, 0.06)
        self.assertEqual(c.holding_period, 5)
        self.assertAlmostEqual(c.first_mort, 0.78, 2)
        self.assertAlmostEqual(c.equity, 0.22, 2)
        self.assertAlmostEqual(c.const, 0.0719, 2)
        self.assertAlmostEqual(c.per_loan_repaid, 0.0695, 2)
        self.assertAlmostEqual(c.mezz_const, 0.08, 2)
        self.assertAlmostEqual(c.per_mezz_loan_repaid, 0.0, 2)

    def test_scenario_1(self):
        self.run_scenario(self.test1_input, self.test1_output)

    def test_scenario_2(self):
        self.run_scenario(self.test2_input, self.test2_output)

    def test_scenario_3(self):
        self.run_scenario(self.test3_input, self.test3_output)

    def test_scenario_4(self):
        self.run_scenario(self.test4_input, self.test4_output)

    def run_scenario(self, input, output):
        c = CalcCapRate(input)
        r = c.iterate_computation()
        self.assertAlmostEqual(r['first_mort'], output['first_mort'], 4)
        self.assertAlmostEqual(r['mezz'], output['mezz'], 4)
        self.assertAlmostEqual(r['sinking_fund_factor'], output['sinking_fund_factor'], 4)
        self.assertAlmostEqual(r['appr_depr_factor'], output['appr_depr_factor'], 4)
        self.assertAlmostEqual(r['calc_yield'], output['calc_yield'], 4)
        self.assertAlmostEqual(r['amort_first_mort'], output['amort_first_mort'], 4)
        self.assertAlmostEqual(r['amort_mezz'], output['amort_mezz'], 4)
        self.assertAlmostEqual(r['appr'], output['appr'], 4)
        self.assertAlmostEqual(r['cap_rate'], output['cap_rate'], 4)
        self.assertAlmostEqual(r['op_cap_rate'], output['op_cap_rate'], 4)
        sum = r['yield_per'] + r['amort_first_mort_per'] + r['amort_mezz_per'] + r['appr_per']
        self.assertAlmostEqual(sum, 1.0, 4)
        return r

    def run_scenario_with_j_factor(self, input, output):
        r = self.run_scenario(input, output)
        self.assertAlmostEqual(r['j_factor'], output['j_factor'], 4)

    def test_base_j_factor(self):
        self.run_scenario_with_j_factor(self.jfactor1_input, self.jfactor1_output)

    def test_j_factor_with_income_appr(self):
        self.run_scenario_with_j_factor(self.jfactor2_input, self.jfactor2_output)

    def run_scenario_with_cash_flow(self, input, output):
        r = self.run_scenario_with_j_factor(input, output)
        self.assertAlmostEqual(r['base_cash_flow'], output['base_cash_flow'], 4)
        self.assertAlmostEqual(r['base_cash_growth'], output['base_cash_growth'], 4)

    def test_cash_flow(self):
        self.run_scenario_with_cash_flow(self.cash_flow_input, self.cash_flow_output)

if __name__ == '__main__':
    unittest.main()

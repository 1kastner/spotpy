import unittest
from spotpy import objectivefunctions as of
import numpy as np

#https://docs.python.org/3/library/unittest.html

class TestObjectiveFunctions(unittest.TestCase):

    # How many digits to match in case of floating point answers
    tolerance = 7

    def setUp(self):
        np.random.seed(42)
        self.simulation = np.random.randn(10)
        self.evaluation = np.random.randn(10)

    def test_bias(self):
        res = of.bias(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, 1.2387193462811703, self.tolerance)

    def test_pbias(self):
        res = of.pbias(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, -156.66937901878677, self.tolerance)

    def test_nashsutcliffe(self):
        res = of.nashsutcliffe(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, -4.1162070769985508, self.tolerance)

    def test_lognashsutcliffe(self):
        # Since log is invalid for negative numbers:
        res = of.lognashsutcliffe(self.evaluation + 3, self.simulation + 3)
        self.assertAlmostEqual(res, -2.3300973555530344, self.tolerance)

    def test_lognashsutcliffe_for_invalid_obs_is_nan(self):
        res = of.lognashsutcliffe(self.evaluation, self.simulation)
        self.assertTrue(np.isnan(res))

    def test_log_p_with_default_scale(self):
        """If the mean of the evaluation function is <0.01, it gets reset to 0.01
        """
        res = of.log_p(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, -13135.8578574, self.tolerance)

    def test_log_p(self):
        # np.mean(evaluation) = -0.79065823458241402
        # np.mean(evaluation + 3) = 2.209341765417586
        # scale should be ~0.22 in this scenario
        res = of.log_p(self.evaluation + 3, self.simulation + 3)
        self.assertAlmostEqual(res, -27.8282293618210, self.tolerance)

    def test_correlationcoefficient_random(self):
        res = of.correlationcoefficient(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, -0.110510977276, self.tolerance)

    def test_correlationcoefficient_for_perfect_positive_is_one(self):
        res = of.correlationcoefficient(self.evaluation, self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

        res = of.correlationcoefficient(self.evaluation, 2*self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

        res = of.correlationcoefficient(self.evaluation, 0.5*self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

    def test_correlationcoefficient_for_perfect_negative_is_minus_one(self):
        res = of.correlationcoefficient(self.evaluation, -self.evaluation)
        self.assertAlmostEqual(res, -1, self.tolerance)

        res = of.correlationcoefficient(self.evaluation, -2*self.evaluation)
        self.assertAlmostEqual(res, -1, self.tolerance)

        res = of.correlationcoefficient(self.evaluation, -0.5*self.evaluation)
        self.assertAlmostEqual(res, -1, self.tolerance)

    def test_rsquared_random(self):
        res = of.rsquared(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, 0.012212676098496588, self.tolerance)

    def test_rsquared_perfect_corr_is_1(self):
        """rsquared for perfect correlation should be 1"""
        res = of.rsquared(self.evaluation, self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

        res = of.rsquared(self.evaluation, 2*self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

        res = of.rsquared(self.evaluation, 0.5*self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

        res = of.rsquared(self.evaluation, -self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

        res = of.rsquared(self.evaluation, -2*self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

        res = of.rsquared(self.evaluation, -0.5*self.evaluation)
        self.assertAlmostEqual(res, 1, self.tolerance)

    def test_mse(self):
        res = of.mse(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, 2.6269877837804119, self.tolerance)

    def test_mse_with_self_is_zero(self):
        res = of.mse(self.evaluation, self.evaluation)
        self.assertAlmostEqual(res, 0.0, self.tolerance)

    def test_rmse(self):
        res = of.rmse(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, 1.6207985019059006, self.tolerance)

    def test_rmse_with_self_is_zero(self):
        res = of.rmse(self.evaluation, self.evaluation)
        self.assertAlmostEqual(res, 0.0, self.tolerance)

    def test_mae(self):
        res = of.mae(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, 1.2387193462811703, self.tolerance)

    def test_mae_with_self_is_zero(self):
        res = of.mae(self.evaluation, self.evaluation)
        self.assertAlmostEqual(res, 0.0, self.tolerance)

    def test_rrmse(self):
        res = of.rrmse(self.evaluation, self.simulation)
        self.assertAlmostEqual(res, -2.0499356498347545, self.tolerance)

    def test_rrmse_with_self_is_zero(self):
        res = of.rrmse(self.evaluation, self.evaluation)
        self.assertAlmostEqual(res, 0.0, self.tolerance)

    def test_rrmse_with_obs_mean_zero_is_nan(self):
        """FIXME: Currently failing because rrmse returns np.inf"""
        evaluation = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
        res = of.rrmse(evaluation, self.simulation)
        print(res)
        self.assertTrue(np.isnan(res))

    def test_length_mismatch_return_nan(self):
        all_funcs = of._all_functions

        for func in all_funcs:
            res = func([0], [0, 1])
            self.assertTrue(np.isnan(res), "Expected np.nan in length mismatch, Got {}".format(res))


if __name__ == '__main__':
    unittest.main()

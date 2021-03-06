"""
:module: SaltNaClRP
:platform: Unix, Windows, OS
:synopsis: Derived salt properties class utilizing Rogers & Pitzer model calculations

.. moduleauthor:: Alex Travesset <trvsst@ameslab.gov>, May2020
.. history:
..                Kevin Marin <marink2@tcnj.edu>, May2020
..                  - Added NaCl parameters from Rogers & Pitzer
..                  - Added Pitzer Parameters along with its pressure and temperature derivatives
"""

import numpy as np
import aqpolypy.units.units as un
import aqpolypy.water.WaterMilleroBP as bp
import aqpolypy.salt.SaltModelPitzer as rp


class NaClPropertiesRogersPitzer(rp.SaltPropertiesPitzer):
    """
    NaCl properties following the work of Rogers and Pitzer :cite:`Rogers1982`

    """

    def __init__(self, tk, pa=1):
        """
        constructor

        :param tk: temperature in kelvin
        :param pa: pressure in atmospheres
        :instantiate: temperature, pressure, stoichiometry coefficients, Pitzer Parameters

        """
        self.tk = tk
        self.pa = pa

        # Calculations nacl parameters and coefficients
        self.mat_stoich = np.array([[1, 1], [1, -1]])

        self.m_ref = 5.550825
        self.y_ref = 10
        self.m_weight = 58.4428
        self.p_ref = np.array([self.m_weight, self.m_ref, self.y_ref])

        # values for ion strength dependence and ion size constants in the extended Pitzer model
        self.alpha_b1 = 2.0
        self.alpha_b2 = 0
        self.alpha_c1 = 0
        self.alpha_c2 = 0
        self.alpha_d1 = 0
        self.alpha_d2 = 0
        self.b_param = 1.2
        self.ion_param = np.array([self.alpha_b1, self.alpha_b2, self.alpha_c1, self.alpha_c2, self.alpha_d1, self.alpha_d2, self.b_param])

        self.cm = np.zeros(28)

        self.cm[0] = 1.0249125e3
        self.cm[1] = 2.7796679e-1
        self.cm[2] = -3.0203919e-4
        self.cm[3] = 1.4977178e-6
        self.cm[4] = -7.2002329e-2
        self.cm[5] = 3.1453130e-4
        self.cm[6] = -5.9795994e-7
        self.cm[7] = -6.6596010e-6
        self.cm[8] = 3.0407621e-8
        self.cm[9] = 5.3699517e-5
        self.cm[10] = 2.2020163e-3
        self.cm[11] = -2.6538013e-7
        self.cm[12] = 8.6255554e-10
        self.cm[13] = -2.6829310e-2
        self.cm[14] = -1.1173488e-7
        self.cm[15] = -2.6249802e-7
        self.cm[16] = 3.4926500e-10
        self.cm[17] = -8.3571924e-13
        # exponent in 18 (19 in reference) is barely visible, it is 5 (confirmed)
        self.cm[18] = 3.0669940e-5
        self.cm[19] = 1.9767979e-11
        self.cm[20] = -1.9144105e-10
        self.cm[21] = 3.1387857e-14
        self.cm[22] = -9.6461948e-9
        self.cm[23] = 2.2902837e-5
        self.cm[24] = -4.3314252e-4
        self.cm[25] = -9.0550901e-8
        self.cm[26] = 8.6926600e-11
        self.cm[27] = 5.1904777e-4

        self.qm = np.zeros(19)

        self.qm[0] = 0.0765
        self.qm[1] = -777.03
        self.qm[2] = -4.4706
        self.qm[3] = 0.008946
        self.qm[4] = -3.3158e-6
        self.qm[5] = 0.2664
        # this value is not provided
        self.qm[6] = 0
        # this value is not provided
        self.qm[7] = 0
        self.qm[8] = 6.1608e-5
        self.qm[9] = 1.0715e-6
        self.qm[10] = 0.00127
        self.qm[11] = 33.317
        self.qm[12] = 0.09421
        self.qm[13] = -4.655e-5
        # this value is not provided
        self.qm[14] = 0
        self.qm[15] = 41587.11
        self.qm[16] = -315.90
        self.qm[17] = 0.8514
        self.qm[18] = -8.3637e-4

        # Pitzer Parameters
        self.tc = 298.15

        self.beta0_1 = self.qm[0] + self.qm[1] * (1 / self.tk - 1 / self.tc) + self.qm[2] * np.log(self.tk / self.tc)
        self.beta0_2 = self.qm[3] * (self.tk - self.tc) + self.qm[4] * (self.tk ** 2 - self.tc ** 2)
        self.beta0 = self.beta0_1 + self.beta0_2

        self.beta1 = self.qm[5] + self.qm[8] * (self.tk - self.tc) + self.qm[9] * (self.tk ** 2 - self.tc ** 2)
        self.beta2 = 0

        self.c_phi_1 = self.qm[10] + self.qm[11] * (1 / self.tk - 1 / self.tc) + self.qm[12] * np.log(self.tk / self.tc)
        self.c_phi = self.c_phi_1 + self.qm[13] * (self.tk - self.tc)
        self.C0 = self.c_phi / 2
        self.C1 = 0
        self.C2 = 0
        self.D0 = 0
        self.D1 = 0
        self.D2 = 0
        self.params = np.array([self.beta0, self.beta1, self.beta2, self.C0, self.C1, self.C2, self.D0, self.D1, self.D2])

        # Pitzer Parameters pressure derivative
        self.pr = un.atm_2_bar(self.pa)
        self.pr_atm = un.atm_2_bar(1)

        self.vp_0 = self.cm[0] + self.cm[1] * self.tk + self.cm[2] * self.tk ** 2 + self.cm[3] * self.tk ** 3
        self.vp_1 = (self.pr - self.pr_atm) * (self.cm[4] + self.cm[5] * self.tk + self.cm[6] * self.tk ** 2)
        self.vp_2 = (self.pr - self.pr_atm) ** 2 * (self.cm[7] + self.cm[8] * self.tk)

        self.vp_sum = self.vp_0 + self.vp_1 + self.vp_2

        self.bp_0 = self.cm[9] + self.cm[10] / (self.tk - 227) + self.cm[11] * self.tk + self.cm[12] * self.tk ** 2 + self.cm[13] / (680 - self.tk)
        self.bp_1_1 = self.cm[14] + self.cm[15] / (self.tk - 227) + self.cm[16] * self.tk + self.cm[17] * self.tk ** 2
        self.bp_1 = (self.bp_1_1 + self.cm[18] / (680 - self.tk)) * (self.pr - self.pr_atm)
        self.bp_2_1 = self.cm[19] + self.cm[20] / (self.tk - 227) + self.cm[21] * self.tk + self.cm[22] / (680 - self.tk)
        self.bp_2 = self.bp_2_1 * (self.pr - self.pr_atm) ** 2

        self.beta0_der_p = self.bp_0 + self.bp_1 + self.bp_2
        self.beta1_der_p = 0
        self.beta2_der_p = 0

        self.cq = self.cm[23] + self.cm[24] / (self.tk - 227) + self.cm[25] * self.tk + self.cm[26] * self.tk ** 2 + self.cm[27] / (680 - self.tk)
        self.cp = 0.5 * self.cq
        self.C0_der_p = self.cp
        self.C1_der_p = 0
        self.C2_der_p = 0

        self.D0_der_p = 0
        self.D1_der_p = 0
        self.D2_der_p = 0

        # calculates the molar volume at infinite dilution (vp)

        # the factor 10 is the conversion from J to bar cm^3
        self.ct = 10 * un.r_gas() * self.tk

        # molar volume water in cm^3/mol
        self.vol_water = 1e6 * bp.WaterPropertiesFineMillero(self.tk, self.pa).molar_volume()

        self.mv_i_0 = self.vp_sum / self.m_ref - self.y_ref * self.vol_water
        self.mv_i_1 = -2 * bp.WaterPropertiesFineMillero(self.tk, self.pa).a_v() * (0.5 * np.log(1 + self.b_param * np.sqrt(self.m_ref)) / self.b_param)
        self.mv_i_2 = -2 * self.ct * (self.m_ref * self.beta0_der_p + self.m_ref ** 2 * self.C0_der_p)
        # this is in cm^3/mol
        self.mv_i = self.mv_i_0 + self.mv_i_1 + self.mv_i_2

        # return in SI m^3
        self.molar_vol_infinite_dilution = 1e-6 * self.mv_i

        # infinite molar volume, convert to cm^3/mol
        self.vp = 1e6 * self.molar_vol_infinite_dilution

        self.params_der_p = np.array([self.vp, self.beta0_der_p, self.beta1_der_p, self.beta2_der_p, self.C0_der_p, self.C1_der_p, self.C2_der_p, self.D0_der_p, self.D1_der_p, self.D2_der_p])

        # Pitzer Parameters temperature derivative
        self.beta0_der_t = 2 * self.qm[4] * self.tk + self.qm[2] / self.tk - self.qm[1] / (self.tk ** 2) + self.qm[3]
        self.beta1_der_t = 2 * self.qm[9] * self.tk + self.qm[8]
        self.beta2_der_t = 0

        self.c_phi_der_t = self.qm[12] / self.tk - self.qm[11] / (self.tk ** 2) + self.qm[13]
        self.C0_der_t = self.c_phi_der_t / 2
        self.C1_der_t = 0
        self.C2_der_t = 0

        self.D0_der_t = 0
        self.D1_der_t = 0
        self.D2_der_t = 0
        self.params_der_t = np.array([self.beta0_der_t, self.beta1_der_t, self.beta2_der_t, self.C0_der_t, self.C1_der_t, self.C2_der_t, self.D0_der_t, self.D1_der_t, self.D2_der_t])

        super().__init__(tk, pa)

    def actual_coefficients(self):
        """
        returns the values of the coefficients as a list

        :return: fitting coefficients for NaCl (list)
        
        """
        return [self.mat_stoich, self.p_ref]

    def pitzer_parameters(self):
        """
        returns the values of the Pitzer Parameters as a list

        :return: Pitzer Parameters for NaCl (array)

        """
        return self.params

    def pitzer_parameters_der_p(self):
        """
        returns the values of the Pitzer Parameters pressure derivative as a list

        :return: Pitzer Parameters pressure derivative for NaCl (array)

        """
        return self.params_der_p

    def pitzer_parameters_der_t(self):
        """
        returns the values of the Pitzer Parameters temperature derivative as a list

        :return: Pitzer Parameters temperature derivative for NaCl (array)

        """
        return self.params_der_t

    def ion_parameters(self):
        """
        returns the values of the ionic strength dependence (alpha) & ion-size (b) parameters as a list

        :return: ionic strength dependence & ion-size parameters for NaCl (array)

        """
        return self.ion_param

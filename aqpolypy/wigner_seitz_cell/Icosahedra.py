"""
:module: Icosahedra
:platform: Unix, Windows, OS
:synopsis: Defines an icosahedral Wigner-Seitz Cell

.. moduleauthor:: Alex Travesset <trvsst@ameslab.gov>, June2020
.. history:
..
"""

import aqpolypy.wigner_seitz_cell.WignerSeitzABC as Ws
import numpy as np


class Icosahedra(Ws.WiSe):

    """ Defines a general Wigner Seitz cell"""

    def __init__(self):
        """
        constructor

        """

        dimension = 3
        num_distinct_wedges = 1

        super().__init__(dimension, num_distinct_wedges)

        psi = np.arccos((1 + np.sqrt(5)) / (2 * np.sqrt(3)))

        def f1(x):
            return 0

        def f2(x):
            return np.arctan(np.tan(psi)/np.cos(x))

        self.wedges[0] = ((0, np.pi/3), (f1, f2))
        self.num_wedges[0] = 120

    def max_theta(self):
        """
        maximum value of the angle :math:`\\theta` for the corresponding wedge

        :return: maximum value of the angle :math:`\\theta` (ndarray)
        """

        b = self.wedges[0][0][1]
        fun = self.wedges[0][1][1]

        return np.array([fun(b)])

    def __str__(self):
        """
        String representation

        :return: name of the class
        """

        return 'Icosahedron Wigner-Seitz cell'

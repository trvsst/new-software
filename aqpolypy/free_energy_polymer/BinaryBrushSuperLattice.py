"""
:module: BinaryBrushSuperLattice
:platform: Unix, Windows, OS
:synopsis: Defines a Spherical Brush in Solvent

.. moduleauthor:: Alex Travesset <trvsst@ameslab.gov>, June2020
.. history:
..
"""

import numpy as np
import scipy.integrate as integrate
from scipy import optimize
from aqpolypy.free_energy_polymer.BrushSolution import MakeBrushSolvent
from aqpolypy.free_energy_polymer.BinaryBrush import BinaryBrush

class BinaryBrushSuperLattice(MakeBrushSolvent):

    """ Defines the free energy of a Brush in a superlattice"""

    def __init__(self, dim, chi, sigma, rad, pol, d_n, ws, **kwargs):
        """
        constructor

        :param dim: plane is d=1, cylinder d=2, sphere d=3
        :param chi: Flory-Huggins Parameter :math:`\\chi`
        :param sigma: grafting density :math:`\\sigma`` in chains/nm :sup:`3`
        :param rad: nanocrystal radius in Angstrom
        :param pol: object of class :class:`PolymerProperties <aqpolypy.polymer.PolymerPropertiesABC.PolymerProperties>`
        :param d_n: nearest neighbor distance for nanocrystals within the lattice in Angstrom
        :param ws: object of class :class:`WiSe <aqpolypy.wigner_seitz_cell.WignerSeitzABC.WiSe>`
        :param kwargs: optional arguments c_s, v_solvent
        """

        super().__init__(dim, chi, sigma, rad, pol, **kwargs)

        # number of components is brush and solvent
        self.num_of_components = 2

        self.d_n = d_n
        # compute the maximum and minimum values of the brush size
        self.h_min = 0.5*self.d_n/np.cos(ws.min_theta()) - self.hat_r*pol.k_length
        self.h_max = 0.5*self.d_n/np.cos(ws.max_theta()) - self.hat_r*pol.k_length

        self.d_min = 2*(self.hat_r*pol.k_length + self.h_min)
        self.d_max = 2*(self.hat_r*pol.k_length + self.h_max)

        # find the lagrange multipliers corresponding to these distances
        lag_ini = 1e-3-chi
        bb = BinaryBrush(dim, chi, sigma, rad, pol, lag_ini)
        lag_opt = bb.optimal_lambda().x
        self.lag_max = bb.determine_lagrange(self.h_max[0])
        self.lag_min = bb.determine_lagrange(self.h_min[0], lag_opt)

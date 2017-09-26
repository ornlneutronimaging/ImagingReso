************
Introduction
************

ImagingReso is an open-source Python library that simulates the neutron
resonance signal for neutron imaging measurements. By defining the sample
information such as density, thickness in the neutron path, and isotopic
ratios of the elemental composition of the material, this package plots
the expected resonance peaks for a selected neutron energy range.
Various sample types such as layers of single elements (Ag, Co, etc. in solid form),
chemical compounds (UO\ :sub:`2`, Gd\ :sub:`2`\O\ :sub:`3`, etc.),
or even multiple layers of both types can be plotted with this package.
Major plotting features include display of the transmission/attenuation in
wavelength, energy, and time scale, and show/hide elemental and
isotopic contributions in the total resonance signal.

The energy dependent cross-section data used in this library are from
`National Nuclear Data Center <http://www.nndc.bnl.gov/>`__, a published
online database. `Evaluated Nuclear Data File
(ENDF/B) <http://www.nndc.bnl.gov/exfor/endf00.jsp>`__ [1] is currently
supported and more evaluated databases will be added in future.

Python packages used are: SciPy [2], NumPy [3], Matplotlib [4], Pandas
[5] and Periodictable [6].

Statement of need
#################

Neutron imaging is a powerful tool to characterize material
non-destructively. And based on the unique resonance features, it is
feasible to identify elements and/or isotopes which resonance with
incident neutrons. However, a dedicated tool for resonance imaging is
missing, and **ImagingReso** we presented here could fill this gap.

Installation instructions
#########################

Install **ImagingReso** by typing the following command in Terminal:

``pip install ImagingReso``

or by typing the following command under downloaded directory in
Terminal:

``python setup.py``

Example usage
#############

Example of usage is presented in ``tutorial.ipynb`` under ``/notebooks``
directory.

Calculation algorithm
#####################

The neutron transmission calculation algorithm of neutron transmission
*T*\ (*E*), is base on Beer-lambert law [7]-[9]:

.. math:: T\left( E \right) =\frac { I\left( E \right)  }{ { I }_{ 0 }\left( E \right)  } =exp\left[ -\sum\nolimits_i { { N }_{ i }{ d }_{ i } } \sum\nolimits_j { { \sigma  }_{ ij }\left( E \right) { A }_{ ij } }  \right]

:math:`N_i` : number of atoms per unit volume of element :math:`i`,

:math:`d_i` : effective thickness along the neutron path of element :math:`i`,

:math:`\sigma_{ij}\left( E \right)` : energy-dependent neutron total cross-section for the isotope :math:`j` of element :math:`i`,

:math:`A_{ij}` : abundance for the isotope :math:`j` of element :math:`i`.

For solid materials the number of atoms per unit volume can be
calculated from:

.. math:: {N_i} = {N_A}{C_i} = \frac{{{N_A}{\rho _i}}}{{\sum\nolimits_j {{m_{ij}}{A_{ij}}} }}

:math:`N_A` : Avogadro’s number,

:math:`C_i` : molar concentration of element :math:`i`,

:math:`\rho_i` : density of the element :math:`i`,

:math:`m_{ij}` : atomic mass values for the isotope :math:`j` of element :math:`i`.


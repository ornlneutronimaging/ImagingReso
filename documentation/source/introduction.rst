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

Announcement
############

A web-based Graphical User Interface (GUI), *Neutron Imaging Toolbox*
(`NEUIT) <https://github.com/ornlneutronimaging/NEUIT>`__), is now available at http://isc.sns.gov/.

Statement of need
#################

Neutron imaging is a powerful tool to characterize material
non-destructively. And based on the unique resonance features, it is
feasible to identify elements and/or isotopes which resonance with
incident neutrons. However, a dedicated tool for resonance imaging is
missing, and **ImagingReso** we presented here could fill this gap.

Community guidelines
####################

**How to contribute**

Clone the code to your own machine, make changes and do a pull request.
We are looking forward to your contribution to this code!

**How to report issues**

Please use 'Issues' tab on Git to submit issue or bug.

**Support**

You can email authors for support.

Installation instructions
#########################

Python 3.5+ is required for installing this package.

Install **ImagingReso** by typing the following command in Terminal:

``conda config --add channels conda-forge``
``conda install imagingreso``

or

``python3 -m pip install ImagingReso``

or by typing the following command under downloaded directory in
Terminal:

``python setup.py``

Example usage
#############

Example of usage is presented at http://imagingreso.readthedocs.io/ .
Same content can also be found in ``tutorial.ipynb`` under ``/notebooks``
in this repository.

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

References
##########

[1] M. B. Chadwick et al., “ENDF/B-VII.1 Nuclear Data for Science and
Technology: Cross Sections, Covariances, Fission Product Yields and
Decay Data,” Nuclear Data Sheets, vol. 112, no. 12, pp. 2887–2996, Dec.
2011.

[2] T. E. Oliphant, “SciPy: Open Source Scientific Tools for Python,”
Computing in Science and Engineering, vol. 9. pp. 10–20, 2007.

[3] S. van der Walt et al., “The NumPy Array: A Structure for Efficient
Numerical Computation,” Computing in Science & Engineering, vol. 13, no.
2, pp. 22–30, Mar. 2011.

[4] J. D. Hunter, “Matplotlib: A 2D Graphics Environment,” Computing in
Science & Engineering, vol. 9, no. 3, pp. 90–95, May 2007.

[5] W. McKinney, “Data Structures for Statistical Computing in Python,”
in Proceedings of the 9th Python in Science Conference, 2010, pp. 51–56.

[6] P. A. Kienzle, “Periodictable V1.5.0,” Journal of Open Source
Software, Jan. 2017.

[7] M. Ooi et al., “Neutron Resonance Imaging of a Au-In-Cd Alloy for
the JSNS,” Physics Procedia, vol. 43, pp. 337–342, 2013.

[8] A. S. Tremsin et al., “Non-Contact Measurement of Partial Gas
Pressure and Distribution of Elemental Composition Using Energy-Resolved
Neutron Imaging,” AIP Advances, vol. 7, no. 1, p. 15315, 2017.

[9] Y. Zhang et al., “The Nature of Electrochemical Delithiation of
Li-Mg Alloy Electrodes: Neutron Computed Tomography and Analytical
Modeling of Li Diffusion and Delithiation Phenomenon,” Journal of the
Electrochemical Society, vol. 164, no. 2, pp. A28–A38, 2017.

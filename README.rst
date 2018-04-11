ImagingReso
===========

.. image:: https://travis-ci.org/ornlneutronimaging/ImagingReso.svg?branch=master
  :target: https://travis-ci.org/ornlneutronimaging/ImagingReso
  :alt: travis

.. image:: https://readthedocs.org/projects/imagingreso/badge/?version=latest
  :target: http://imagingreso.readthedocs.io/en/latest/?badge=latest
  :alt: readthedocs

.. image:: https://codecov.io/gh/ornlneutronimaging/ImagingReso/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ornlneutronimaging/ImagingReso
  :alt: codecov

.. image:: http://joss.theoj.org/papers/997d09281a9d76e95f4ec4d3279eeb8c/status.svg
  :target: http://joss.theoj.org/papers/997d09281a9d76e95f4ec4d3279eeb8c
  :alt: DOI

.. image:: https://img.shields.io/pypi/v/ImagingReso.svg
  :target: https://pypi.python.org/pypi/ImagingReso
  :alt: pypi

.. image:: https://anaconda.org/conda-forge/imagingreso/badges/version.svg
  :target: https://anaconda.org/conda-forge/imagingreso
  :alt: conda

.. image:: https://anaconda.org/conda-forge/imagingreso/badges/latest_release_date.svg
  :target: https://anaconda.org/conda-forge/imagingreso
  :alt: latest_release_date

.. image:: https://anaconda.org/conda-forge/imagingreso/badges/downloads.svg
  :target: https://anaconda.org/conda-forge/imagingreso
  :alt: downloads

.. image:: https://anaconda.org/conda-forge/imagingreso/badges/platforms.svg
  :target: https://anaconda.org/conda-forge/imagingreso
  :alt: platform

.. image:: https://anaconda.org/conda-forge/imagingreso/badges/license.svg
  :target: https://anaconda.org/conda-forge/imagingreso
  :alt: license

Abstract
--------

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
(ENDF/B-VII.1) <http://www.nndc.bnl.gov/exfor/endf00.jsp>`__ [1] is currently
supported and more evaluated databases will be added in future.

Python packages used are: SciPy [2], NumPy [3], Matplotlib [4], Pandas
[5] and Periodictable [6].

Statement of need
-----------------

Neutron imaging is a powerful tool to characterize material
non-destructively. And based on the unique resonance features, it is
feasible to identify elements and/or isotopes which resonance with
incident neutrons. However, a dedicated tool for resonance imaging is
missing, and **ImagingReso** we presented here could fill this gap.

Community guidelines
--------------------

**How to contribute**

Clone the code to your own machine, make changes and do a pull request.
We are looking forward to your contribution to this code!

**How to report issues**

Please use 'Issues' tab on Git to submit issue or bug.

**Support**

You can email authors for support.

Installation instructions
-------------------------

Python 3.x is required for installing this package.

Install **ImagingReso** by typing the following command in Terminal:

.. code-block:: bash

   $ pip install ImagingReso

or

.. code-block:: bash

   $ conda config --add channels conda-forge
   $ conda install imagingreso

or by typing the following command under downloaded directory in
Terminal:

.. code-block:: bash
   
   $ python setup.py

Example usage
-------------

Example of usage is presented at http://imagingreso.readthedocs.io/ .
Same content can also be found in ``tutorial.ipynb`` under ``/notebooks``
in this repository.

Calculation algorithm
---------------------

The calculation algorithm of neutron transmission *T*\ (*E*),
is base on Beer-Lambert law [7]-[9]:

.. figure:: https://github.com/ornlneutronimaging/ImagingReso/blob/master/documentation/source/_static/Beer_lambert_law_1.png
   :alt: Beer-lambert Law 1
   :align: center

where

N\ :sub:`i` : number of atoms per unit volume of element *i*,

d\ :sub:`i` : effective thickness along the neutron path of element *i*,

σ\ :sub:`ij` (E) : energy-dependent neutron total cross-section for the isotope *j* of element *i*,

A\ :sub:`ij` : abundance for the isotope *j* of element *i*.

For solid materials, the number of atoms per unit volume can be
calculated from:

.. figure:: https://github.com/ornlneutronimaging/ImagingReso/blob/master/documentation/source/_static/Beer_lambert_law_2.png
   :align: center
   :alt: Beer-lambert law 2

where

N\ :sub:`A` : Avogadro’s number,

C\ :sub:`i` : molar concentration of element *i*,

ρ\ :sub:`i` : density of the element *i*,

m\ :sub:`ij` : atomic mass values for the isotope *j* of element *i*.

References
----------

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

Meta
----

Yuxuan Zhang - zhangy6@ornl.gov

Jean Bilheux - bilheuxjm@ornl.gov

Distributed under the BSD license. See ``LICENSE.txt`` for more information

https://github.com/ornlneutronimaging/ImagingReso

Publication
-----------

Yuxuan Zhang and Jean Bilheux, "ImagingReso: A Tool for Neutron Resonance Imaging", *The Journal of Open Source Software*, 2 (2017) 407, doi:10.21105/joss.00407

Acknowledgements
----------------

This work is sponsored by the Laboratory Directed Research and
Development Program of Oak Ridge National Laboratory, managed by
UT-Battelle LLC, under Contract No. DE-AC05-00OR22725 with the U.S.
Department of Energy. The United States Government retains and the
publisher, by accepting the article for publication, acknowledges
that the United States Government retains a non-exclusive, paid-up,
irrevocable, worldwide license to publish or reproduce the published
form of this manuscript, or allow others to do so, for United States
Government purposes. The Department of Energy will provide public
access to these results of federally sponsored research in accordance
with the DOE Public Access Plan(http://energy.gov/downloads/doe-public-access-plan).


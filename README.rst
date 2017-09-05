ImagingReso
==========

.. image:: https://travis-ci.org/ornlneutronimaging/ImagingReso.svg?branch=master
  :target: https://travis-ci.org/ornlneutronimaging/ImagingReso
    
.. image:: https://codecov.io/gh/ornlneutronimaging/ImagingReso/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ornlneutronimaging/ImagingReso
  
.. image:: https://readthedocs.org/projects/imagingreso/badge/?version=latest
  :target: http://imagingreso.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
  

Abstract
--------
  
Here we present an open-source Python library which focuses on simulating the neutron resonance signal 
for neutron imaging measurements. In this package, by defining the sample information such as density, 
thickness in the neutron path and isotopic ratios of the elemental composition of the material, one can 
plot of expected resonance peaks for a selected neutron energy range. Various sample types such as 
layers of single elements (Ag, Co, etc. in solid form), chemical compounds (UO<sub>3</sub>, 
Gd<sub>2</sub>O<sub>3</sub>, etc.), or even multiple layers of both types. Major plotting features include 
display of the transmission/attenuation in wavelength/energy/time scale, show/hide elemental and isotopic contributions 
in the total resonance signal.

The energy dependent cross-section data used in this library are from [National Nuclear Data Center](http://www.nndc.bnl.gov/), 
a published online database. [Evaluated Nuclear Data File (ENDF/B)](http://www.nndc.bnl.gov/exfor/endf00.jsp) [1] 
is currently supported and more evaluated databases will be added in future.

Python packages used are: SciPy [2], NumPy [3], Matplotlib [4], Pandas [5] and Periodictable [6].


Statement of need
-----------------

Neutron imaging is a powerful tool to characterize material non-destructively. And based on the unique resonance features, 
it is feasible to identify elements and/or isotopes which resonance with incident neutrons. However, a dedicated tool 
for resonance imaging is missing, and _ImagingReso_ we presented here could fill this gap.


Installation instructions
-------------------------

Install _ImagingReso_ by typing the following command in Terminal:


.. code-block:: bash
  
  $ pip install ImagingReso`


or by typing the following command under downloaded directory in Terminal: 


.. code-block:: bash

  $ python setup.py`


Example
-------

See the documentation

.. image:: https://readthedocs.org/projects/imagingreso/badge/?version=latest
  :target: http://imagingreso.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


Calculation algorithm
---------------------

The neutron transmission calculation algorithm of neutron transmission *T*(*E*), is base on Beer-Lambert law [7]-[9]:

.. image:: documentation/source/_static/Beer_lambert_law_1.png
   :alt: Beer Lambert Law 1
   :align: center
 
N :sub:`i` : number of atoms per unit volume of element *i*, 

d :sub:`i` : effective thickness along the neutron path of element *i*,

σ :sub:`ij` (E) : energy-dependent neutron total cross-section for the isotope *j* of element *i*, 

A :sub:`ij` : abundance for the isotope *j* of element *i*. 


For solid materials the number of atoms per unit volume can be calculated from:

.. image:: documentation/source/_static/Beer_lambert_law_2.png
   :align: center
   :alt: Beer Lambert law 2

N :sub:`A` : Avogadro’s number,

C :sub:`i` : molar concentration of element *i*,

ρ :sub:`i` : density of the element *i*,

m :sub:`ij` : atomic mass values for the isotope *j* of element *i*.


Acknowledgements
----------------

This work is sponsored by the Laboratory Directed Research and Development Program of Oak Ridge National Laboratory, 
managed by UT-Battelle LLC, for DOE. 
Part of this research is supported by the U.S. Department of Energy, Office of Science, Office of Basic Energy Sciences, 
User Facilities under contract number DE-AC05-00OR22725.


References
----------

[1]	M. B. Chadwick et al., “ENDF/B-VII.1 Nuclear Data for Science and Technology: Cross Sections, Covariances, Fission Product Yields and Decay Data,” Nuclear Data Sheets, vol. 112, no. 12, pp. 2887–2996, Dec. 2011.

[2]	T. E. Oliphant, “SciPy: Open Source Scientific Tools for Python,” Computing in Science and Engineering, vol. 9. pp. 10–20, 2007.

[3]	S. van der Walt et al., “The NumPy Array: A Structure for Efficient Numerical Computation,” Computing in Science & Engineering, vol. 13, no. 2, pp. 22–30, Mar. 2011.

[4]	J. D. Hunter, “Matplotlib: A 2D Graphics Environment,” Computing in Science & Engineering, vol. 9, no. 3, pp. 90–95, May 2007.

[5]	W. McKinney, “Data Structures for Statistical Computing in Python,” in Proceedings of the 9th Python in Science Conference, 2010, pp. 51–56.

[6]	P. A. Kienzle, “Periodictable V1.5.0,” Journal of Open Source Software, Jan. 2017.

[7]	M. Ooi et al., “Neutron Resonance Imaging of a Au-In-Cd Alloy for the JSNS,” Physics Procedia, vol. 43, pp. 337–342, 2013.

[8]	A. S. Tremsin et al., “Non-Contact Measurement of Partial Gas Pressure and Distribution of Elemental Composition Using Energy-Resolved Neutron Imaging,” AIP Advances, vol. 7, no. 1, p. 15315, 2017.

[9]	Y. Zhang et al., “The Nature of Electrochemical Delithiation of Li-Mg Alloy Electrodes: Neutron Computed Tomography and Analytical Modeling of Li Diffusion and Delithiation Phenomenon,” Journal of the Electrochemical Society, vol. 164, no. 2, pp. A28–A38, 2017.



Meta
----

Yuxuan Zhang - `zhangy6@ornl.gov` 
Jean Bilheux - 'bilheuxjm@ornl.gov'


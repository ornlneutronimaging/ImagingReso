[![Build Status](https://travis-ci.org/ornlneutronimaging/ImagingReso.svg?branch=master)](https://travis-ci.org/ornlneutronimaging/ImagingReso)
[![codecov](https://codecov.io/gh/ornlneutronimaging/ImagingReso/branch/master/graph/badge.svg)](https://codecov.io/gh/ornlneutronimaging/ImagingReso)
[![Documentation Status](https://readthedocs.org/projects/imagingreso/badge/?version=latest)](http://imagingreso.readthedocs.io/en/latest/?badge=latest)

# ImagingReso

This package provides various feasibility for plotting and manipulating 
neutron resonance signal from the published online database,
[National Nuclear Data Center](http://www.nndc.bnl.gov/).

[Evaluated Nuclear Data File (ENDF.VIII)](http://www.nndc.bnl.gov/exfor/endf00.jsp) 
is currently supported and more database will be supported in the future.

In this package, by defining the sample information such as density, effective thickness and isotopic ratios of each element,
one can easily obtain an expected plot of resonance signal of various sample types 
such as layers of single element (Ag, Co, etc. in solid form),
chemical compound (UO<sub>3</sub>, Gd<sub>2</sub>O<sub>3</sub>), or even multiple layers including both types). 
Plotting options such as transmission or attenuation as y-axis and energy or wavelength as x-axis are provided. 
One can also make the program to show/hide elemental and isotopic contributions in the total resonance signal.

### Calculation Algorithm

The neutron transmission calculation algorithm is base on Beer-Lambert law:

![BeerLambert_law_1](documentation/source/_static/Beer_lambert_law_1.png)

*N<sub>i</sub>* : number of atoms of element *i* per unit volume, 

*d<sub>i</sub>* : the effective thickness element *i* integrated along the neutron path, 

*σ<sub>ij</sub>(E)* : the energy-dependent neutron attenuation cross-section, 

*A<sub>ij</sub>* : abundance for the isotope *j* of element *i*. 


For solid materials the number of atoms per unit volume can be calculated from:

![BeerLambert_law_2](documentation/source/_static/Beer_lambert_law_2.png)

*ρ<sub>i</sub>* : known density of the material,

*m<sub>ij</sub>* : atomic mass values.





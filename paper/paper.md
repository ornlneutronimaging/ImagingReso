---
title: 'ImagingReso: A Tool for Neutron Resonance Imaging'
tags:
  - neutron resonance
  - neutron imaging
authors:
 - name: Yuxuan Zhang
   orcid: 0000-0002-0083-1408
   affiliation: 1
 - name: Jean Bilheux
   orcid: 0000-0003-2172-6487
   affiliation: 1
affiliations:
 - name: Oak Ridge National Laboratory
   index: 1
   
date: 17 November 2017
output: html_document
bibliography: paper.bib
---

# Summary

ImagingReso is an open-source Python library that simulates the neutron
resonance signal for neutron imaging measurements. By defining the sample
information such as density, thickness in the neutron path, and isotopic
ratios of the elemental composition of the material, this package plots
the expected resonance peaks for a selected neutron energy range.
Various sample types such as layers of single elements (Ag, Co, etc. in solid form),
chemical compounds (UO<sub>3</sub>, Gd<sub>2</sub>O<sub>3</sub>, etc.),
or even multiple layers of both types can be plotted with this package.
Major plotting features include display of the transmission/attenuation in
wavelength, energy, and time scale, and show/hide elemental and
isotopic contributions in the total resonance signal.

The energy dependent cross-section data used in this library are from
[National Nuclear Data Center](http://www.nndc.bnl.gov/), a published
online database. [Evaluated Nuclear Data File 
(ENDF/B)](http://www.nndc.bnl.gov/exfor/endf00.jsp) [@Chadwick2011] is currently
supported and more evaluated databases will be added in future.

Python packages used are: SciPy [@Oliphant2007], NumPy [@Stéfan van der Walt2011], 
Matplotlib [@Hunter2007], Pandas [@McKinney2010] and Periodictable [@kienzle_p_a_2017_840347].

The energy dependent cross-section data used in this library are from 
[National Nuclear Data Center](http://www.nndc.bnl.gov/), an online database 
published by Brookhaven National Laboratory. 
[Evaluated Nuclear Data File (ENDF/B)](http://www.nndc.bnl.gov/exfor/endf00.jsp) 
is currently supported and more evaluated databases will be added in the future.

The neutron transmission calculation algorithm of neutron transmission *T*(*E*), 
is base on Beer-Lambert law [@Ooi2013;@Tremsin2017;@Zhang2017]:

![Figure_1](https://github.com/ornlneutronimaging/ImagingReso/blob/master/documentation/source/_static/Beer_lambert_law_1.png)

*N<sub>i</sub>* : number of atoms per unit volume of element *i*, 

*d<sub>i</sub>* : effective thickness along the neutron path of element *i*,

*σ<sub>ij</sub>(E)* : energy-dependent neutron total cross-section for the isotope *j* of element *i*, 

*A<sub>ij</sub>* : abundance for the isotope *j* of element *i*. 

For solid materials the number of atoms per unit volume can be calculated from:

![Figure_2](https://github.com/ornlneutronimaging/ImagingReso/blob/master/documentation/source/_static/Beer_lambert_law_2.png)

*N<sub>A</sub>* : Avogadro’s number,

*C<sub>i</sub>* : molar concentration of element *i*,

*ρ<sub>i</sub>* : density of the element *i*,

*m<sub>ij</sub>* : atomic mass values for the isotope *j* of element *i*.

# Acknowledgements
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

# References



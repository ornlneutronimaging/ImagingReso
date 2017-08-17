---
title: 'ImagingReso: A tool for neutron resonance imaging'
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
   
date: 14 August 2017
bibliography: paper.bib
---

# Summary

This package provides feasibility of plotting and manipulating 
neutron resonance signal from the published online database,
[National Nuclear Data Center](http://www.nndc.bnl.gov/).

[Evaluated Nuclear Data File (ENDF.VIII)](http://www.nndc.bnl.gov/exfor/endf00.jsp) 
is currently supported and more database will be supported in future.

In this package, by defining the sample information such as density, effective thickness and isotopic ratios of each element,
one can easily obtain a plot of expected resonance signal of various sample types 
such as layers of single element (Ag, Co, etc. in solid form),
chemical compound (UO<sub>3</sub>, Gd<sub>2</sub>O<sub>3</sub>, etc.), or even multiple layers including both types. 

Plotting options such as transmission or attenuation as y-axis and energy or wavelength as x-axis are provided. 
One can also make the program to show/hide elemental and isotopic contributions in the total resonance signal.


# References
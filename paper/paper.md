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
   
date: 7 September 2017
bibliography: paper.bib
---

# Summary

ImagingReso is an open-source Python library that simulates the neutron 
resonance signal for neutron imaging measurements. By defining the sample 
information such as density, thickness in the neutron path, and isotopic 
ratios of the elemental composition of the material, this package plots 
the expected resonance peaks for a selected neutron energy range. Various 
sample types such as layers of single elements (Ag, Co, etc. in solid form), 
chemical compounds (UO<sub>3</sub>, Gd<sub>2</sub>O<sub>3</sub>, etc.), 
or even multiple layers of both types can be plotted with this package. 
Major plotting features include display of the transmission/attenuation 
in wavelength, energy, and time scale, and show/hide elemental and isotopic 
contributions in the total resonance signal.

The energy dependent cross-section data used in this library are from 
[National Nuclear Data Center](http://www.nndc.bnl.gov/), an online database 
published by Brookhaven National Laboratory. 
[Evaluated Nuclear Data File (ENDF/B)](http://www.nndc.bnl.gov/exfor/endf00.jsp) 
is currently supported and more evaluated databases will be added in the future.

# References
paper.bib

# Notice of Copyright
This manuscript has been authored by UT-Battelle, LLC under Contract 
No. DE-AC05-00OR22725 with the U.S. Department of Energy. The United 
States Government retains and the publisher, by accepting the article 
for publication, acknowledges that the United States Government retains 
a non-exclusive, paid-up, irrevocable, worldwide license to publish 
or reproduce the published form of this manuscript, or allow others 
to do so, for United States Government purposes. The Department of Energy 
will provide public access to these results of federally sponsored 
research in accordance with the DOE Public Access Plan 
(http://energy.gov/downloads/doe-public-access-plan).

# Acknowledgements

This work is sponsored by the Laboratory Directed Research and
Development Program of Oak Ridge National Laboratory, managed by
UT-Battelle LLC, for DOE. Part of this research is supported by the U.S.
Department of Energy, Office of Science, Office of Basic Energy
Sciences, User Facilities under contract number DE-AC05-00OR22725.
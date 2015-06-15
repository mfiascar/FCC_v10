# FCC_v10
Files for FCC-hh collimation studies, v10_roundracetrack_lhc.100.12

This repository contains all input files needed for performing tracking simulations of the FCC-hh collimation system.
The lattice version used is v10_roundracetrack_lhc_100.12 and was provided by Barbara Dalena (can be found in /afs/cern.ch/user/d/dalena/public/fcc/optics/LATTICE_V10/). 
The lattice includes two high-beta insertions and two collimation insertions (right now being the same: betatron collimation scaled from the LHC using a scaling factor of 5 for beta functions and insertion lenghts).

The repositor containes the following directories:

- MADX: all madx input files from Barbara, plus scripts to add additional collimators (TCTs and TCLDs in the DS after the betatron collimation) and to generate a preliminary aperture model for the machine. You find in this directory all scripts needed to generate the SixTrack input file (fort.2), as well as the input files needed to run BeamLossPattern (aperture and survey files). See MADX/README for more details.




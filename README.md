# FCC_v10
Files for FCC-hh collimation studies, v10_roundracetrack_lhc.100.12

This repository contains all input files needed for performing tracking simulations of the FCC-hh collimation system.
The lattice version used is v10_roundracetrack_lhc_100.12 and was provided by Barbara Dalena (can be found in /afs/cern.ch/user/d/dalena/public/fcc/optics/LATTICE_V10/). 
The lattice includes two high-beta insertions and two collimation insertions (right now being the same: betatron collimation scaled from the LHC using a scaling factor of 5 for beta functions and insertion lenghts).

The repositor containes the following directories:

- MADX: all madx input files from Barbara, plus scripts to add additional collimators (TCTs and TCLDs in the DS after the betatron collimation) and to generate a preliminary aperture model for the machine. You find in this directory all scripts needed to generate the SixTrack input file (fort.2), as well as the input files needed to run BeamLossPattern (aperture and survey files). See MADX/README for more details.

- Betatron_IR2*: contain the input for the simulations, for different collimation layouts.
  * BetatronIR2: betatron cleaning only (19 collimators)
  * BetatronIR2_plusTCT: betatron cleaning + tertiary collimators in IRs
  * BetatronIR2_plusDS_v*: betatron cleaning + one or two TCLDs in DS (v1.0, v1.1, v1.2: one DS collimator in cells 8 or 9; v2.0, v2.1: two DS collimators in cells 8,10 or 9,11)





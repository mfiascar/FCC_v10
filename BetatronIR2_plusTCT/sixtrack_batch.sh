#!/bin/bash
 
# ALWAYS check:
# beam 1 or 2
# batch queue
# LocalPWD : where on the mac should the files be copied. Does the directory exist?
# post-processing programs to run
# which output files should be copied back
# should previous dirs run* be deleted


PWD=`pwd`

#Clean input directory
inputDir="/afs/cern.ch/user/m/mfiascar/workdir/Accelerator/Simulations/FCC/v10_fromBarbara/BetatronIR2_plusTCT"

#Output directory
#outputDir="/afs/cern.ch/user/m/mfiascar/workdir/Accelerator/Simulations/Outputs/" #used only if LXPLUS
LocalPWD="/home/mfiascar/Physics/Accelerator/Simulation/FCC/v10/BetatronIR2_plusTCT" #used for local machine

#directory where all executables are
executeDir="/afs/cern.ch/user/m/mfiascar/workdir/Accelerator/Simulations/fromRoderik/executables"

queue=1nd

beam=1
LIMITLOW=1
LIMITHIGH=1000

exec="${executeDir}/SixTrack_4518_cernlib_coll_gfortran_O4"
beamLossPatt="${executeDir}/BeamLossPattern_gcc2.9"
cleanInel="${executeDir}/CleanInelastic_2013-08-19"
cleanCollScatter="${executeDir}/CleanCollScatter_2014.09.10"
cleanCollSum="${executeDir}/correct_coll_summary.sh"


echo $PWD
#cp -r $inputDir/clean_input $outputDir
ssh mfiascar@PCBE13991 "mkdir -p ${LocalPWD}"
scp -r $inputDir/clean_input mfiascar@PCBE13991:"${LocalPWD}"

#scp $cleanInel mfiascar@PCBE13991:"${LocalPWD}clean_input"
scp $exec mfiascar@PCBE13991:"${LocalPWD}clean_input"
#scp $beamLossPatt mfiascar@PCBE13991:"${LocalPWD}clean_input"
#scp $cleanCollScatter mfiascar@PCBE13991:"${LocalPWD}clean_input"
#scp $cleanCollSum mfiascar@PCBE13991:"${LocalPWD}clean_input"


# copy this script
thisscript=`basename $0`
thisdir=`dirname $0`
scp  $thisdir/$thisscript mfiascar@PCBE13991:"${LocalPWD}"clean_input
#cp $thisdir/$thisscript "${outputDir}clean_input"

rm -r LSFJOB_*

for ((a = LIMITLOW; a <= LIMITHIGH ; a++))
  do
  index=$a
  zero=0
  while [ "${#index}" -lt "4" ]
    do
    index=$zero$index
  done 
  rm -r run$index
  mkdir run$index
  echo run$index

  cat > run$index/SixTr--$index.job << EOF
  #!/bin/bash

  echo "Starting my batch script"
  export CWD=\`pwd\`

  echo "Current directory is \$CWD"
  cp $inputDir/clean_input/* .

  $exec > screenout

  echo "done sixTrack"
  ##gunzip SurveyWithCrossing_XP_lowb_$beam.dat.gz
  #cp SurveyWithCrossing_slices_HLLHCV1_B${beam}.dat SurveyWithCrossing_XP_lowb.dat

  #$beamLossPatt lowb tracks2.dat BLP_out allapert.b$beam
  #echo "done beamLossPatt"
  ## remove binary characters in LPI file:
  #perl -pi -e 's/\0/ /g' LPI_BLP_out.s 

##  ./CleanInelastic FLUKA_impacts.dat LPI_BLP_out.s CollPositions.${beam}.dat coll_summary.dat
  #$cleanInel FLUKA_impacts.dat LPI_BLP_out.s CollPositions.b${beam}.dat coll_summary.dat
  #$cleanCollScatter Coll_Scatter.dat LPI_BLP_out.s CollPositions.b${beam}.dat coll_summary.dat
  #echo "done cleanInel and cleanCollScatter"

## create clean coll_summary with awk script
##  ./awkCollSummary.sh impacts_real.dat
  #$cleanCollSum
  #echo "done cleanCollSum"

  #./FirstImpacts--Average.sh > first_imp_average.dat
  #echo "done Average"

##  ./get_all_TCTVA5_tracks.sh 

  #ls -lh

  ##mkdir $outputDir/run$index/
  ##cp  Coll_Scatter_real* collgaps.dat coll_summary.dat survival.dat LPI* impacts_all* first_imp_average.dat $outputDir/run$index/
  mkdir run$index/
#  cp  Coll_Scatter_real* collgaps.dat coll_summary.dat survival.dat LPI* impacts_all* impacts_real.dat first_imp_average.dat FirstImpacts.dat FLUKA_impacts.dat dist0.dat efficiency*.dat run$index/
  cp  Coll_Scatter* collgaps.dat coll_summary.dat FirstImpacts.dat FLUKA_impacts.dat dist0.dat efficiency*.dat run$index/
  echo "copied all files"

  #gzip $outputDir/run${index}/*
  gzip run${index}/*

  scp -r run${index} mfiascar@PCBE13991:"${LocalPWD}"
  rm -r run${index}
#  cp -r $PWD/run${index} $outputDir
#  rm -r $PWD/run${index}/*
###  cp dist0.dat $PWD/run${index}/dist0.old.dat
  exit
EOF
if [ -d "run$index" ]; then
    cd run$index
    chmod 777 SixTr--$index.job
    bsub -q $queue -o /dev/null -e /dev/null -sp 100 -R "rusage[pool=10000]" SixTr--$index.job
    # -o /dev/null -e /dev/null: switches off email notification
    # -sp : set priority, between 1 and 100
    # -R "rusage[pool=30000]" : allocate 30 GB hard drive space / it was 50
    sleep 1
    cd ..
fi
  
done

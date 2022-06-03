#!/bin/bash -l

# loop to launch samples to run IMP
for i in $(cat toRun)
do
    workdir=$PWD
    cd $i
    sbatch ./launchIMP.sh
    cd $workdir
done

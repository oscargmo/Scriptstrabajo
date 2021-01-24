#!/bin/bash

for i in {001..050}; do
#	sbatch H_JOBID$i/SBATCH_H_$i.sh
	sbatch Fe_JOBID$i/SBATCH_Fe_$i.sh
done

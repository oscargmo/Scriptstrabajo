#!/bin/bash

for i in {001..050}; do
#	sbatch SBATCH_H_1-10TeV_$i.sh
#	sbatch SBATCH_Fe_1-10TeV_$i.sh
#	sbatch SBATCH_H_10-100TeV_$i.sh
#       sbatch SBATCH_Fe_10-100TeV_$i.sh
#	sbatch SBATCH_H_100-1000TeV_$i.sh
#	sbatch SBATCH_Fe_100-1000TeV_$i.sh
#       sbatch SBATCH_H_1000-10000TeV_$i.sh
# 	sbatch SBATCH_Fe_1000-10000TeV_$i.sh
#	sbatch SBATCH_H_10000-100000TeV_$i.sh
	sbatch SBATCH_Fe_10000-100000TeV_$i.sh
done

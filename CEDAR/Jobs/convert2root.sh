#!/bin/bash

for i in {101..150}; do
	sbatch CSK2ROOT_H_10000-100000TeV_$i.sh
#	sbatch CSK2ROOT_Fe_10000-100000TeV_$i.sh	
done

#!/bin/bash

for i in {001..050};do
	echo "####################################################################### Archivo $i "
#	tail H_1000-10000TeV_$i.out
	tail Fe_1000-10000TeV_$i.out
done

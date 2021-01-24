#!/bin/bash

carpeta='AnalisisEPOS-LHC_vertical_10000-100000TeV'
mkdir $PWD/$carpeta

for i in {001..050};do
	cp Fe_JOBID$i/Mathusla_toymodel_Zegdeg_0.0_20.0_events_0_1_iron_v8.root $carpeta/Mathusla_toymodel_Zegdeg_0.0_20.0_events_0_1_iron_v8_ID$i.root
#	mv H_JOBID$i/Mathusla_toymodel_Zegdeg_0.0_20.0_events_0_15_proton_v8.root $carpeta/Mathusla_toymodel_Zegdeg_0.0_20.0_events_0_15_proton_v8_ID$i.root
done


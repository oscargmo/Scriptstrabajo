# -*- coding: utf-8 -*-
import numpy as np
import os

# Ruta al directorio de trabajo
work_dir = str(os.getcwd()) + "/"
print("\nWORKING DIRECTORY:" + work_dir)
primario = "Fe_"
# Numero atomico y Peso atomico
Z, A = 26,56  
# Enería min y max (TeV) 
E_min, E_max = 10000, 100000
# Zenith min y max (Deg)
T_min, T_max = 0, 20
# Número de casacadas por corrida y Num. de cards a crear
nshow, N_cards = 1, 200
time_cpu = "--time=36:00:00"
time_csk2root = "--time=00:10:00"
# Directorio donde se guardaran los datos
energy_range = str(E_min) + "-" + str(E_max) + "TeV"
card_name = primario + energy_range
root_file = "Z=" + str(Z) + "_A=" + str(A) + "_NSHOW=" + str(nshow) + "_"
# Nombre del ejecutable que creamos al compilar CORSIKA
ejecutable = "./corsika77100Linux_SIBYLL_fluka < "
# Verificamos que esxista el directorio, si no existe se creará
if not os.path.isdir(work_dir + energy_range):
        print("\nDid not find any output directory, creating new one!")
        os.system("mkdir -p " + work_dir + energy_range)
# CORSIKA ID del primario
if Z == 0:
    prmpar = 1
elif Z == 1:
    prmpar = 14
else:
    prmpar = A*100 + Z
    
# Generamos las semillas para el Monte Carlo       
seed1 = 10000
seed2 = 10001
seed3 = 10002
# Inicializamos el areglo para las cards
run_num = np.arange(N_cards) +  1
print(run_num)

for i in range(len(run_num)):
    file = open(work_dir + card_name + "_" + str(i+1).zfill(3) + ".input", "w")
    file.write("RUNNR   " + str(i+1) + "                            run number" + os.linesep)
    file.write("EVTNR   1                            number of first shower event" + os.linesep)
    file.write("NSHOW   " + str(nshow) + "                       number of showers to generate" + os.linesep)
    file.write("PRMPAR  " + str(prmpar) + "                           particle type of prim. particle" + os.linesep)
    file.write("ESLOPE  -2.0" + "                         slope of primary energy spectrum"  + os.linesep)
    file.write("ERANGE  " + str(E_min) + ".E3  " + str(E_max)  + ".E3           energy range of primary particle (GeV)" + os.linesep)
    file.write("THETAP  " + str(T_min) + ".  " + str(T_max) + ".                 range of zenith angle (degree)" + os.linesep)
    file.write("PHIP    0.  360.                     range of azimuth angle (degree)" + os.linesep)
    file.write("SEED    " + str(seed1 + i )  + "    0     0              seed for hadronic part" + os.linesep)
    file.write("SEED    " + str(seed2 + i )+ "    0     0              seed for EGS4 part" + os.linesep)
    file.write("SEED    " + str(seed3 + i )  + "    0     0              seed for Cherenkov part" + os.linesep)
    file.write("OBSLEV  436.E2                        observation level (in cm)" + os.linesep)
    file.write("FIXHEI  0.  0                         If FIXHEI = 0., the height of the first interaction is varied at random according to the appropriate mean free path." + os.linesep)
    file.write("FIXCHI  0.                            starting altitude (g/cm**2)" + os.linesep)
    file.write("FLUDBG  F                             FLUKA debug " + os.linesep)
    file.write("MAGNET  22.2  41.9                    magnetic field" + os.linesep)
    file.write("HADFLG  0  0  0  0  0  2              flags hadr.interact.&fragmentation" + os.linesep)
    file.write("HILOW   200.                          Transition Energy lab between Models (GeV)" + os.linesep)
    file.write("ECUTS   0.10 0.10 0.003 0.003 " + "        energy cuts for particles (GeV)"+ os.linesep)
    file.write("SIBYLL  T  0" + os.linesep)
    file.write("SIBSIG  T" + os.linesep)
    file.write("MUADDI  T                             additional info for muons" + os.linesep)
    file.write("MUMULT  T                             muon multiple scattering angle" + os.linesep)
    if T_min == 70 :
        file.write("ELMFLG  F   T                         em. interaction flags (NKG,EGS), NKG option must be disabbled when using CURVED option" + os.linesep)
        file.write("*RADNKG  2.00E4                        outer radius for NKG lat.dens.distr., NKG option must be disabbled when using CURVED option" + os.linesep)
    else:
        file.write("ELMFLG  T   T                         em. interaction flags (NKG,EGS), NKG option must be disabbled when using CURVED option" + os.linesep)
        file.write("RADNKG  2.00E4                        outer radius for NKG lat.dens.distr., NKG option must be disabbled when using CURVED option" + os.linesep)
    file.write("STEPFC  1.0                           mult. scattering step length fact." + os.linesep)
    file.write("ARRANG  0.                            rotation of array to north" + os.linesep)
    file.write("LONGI   F  20.  F  F                  longit.distr. & step size & fit & out" + os.linesep)
    file.write("ECTMAP  1.E2                          cut on gamma factor for printout" + os.linesep)
    file.write("MAXPRT  1                             max. number of printed events" + os.linesep)
    file.write("DIRECT  " + work_dir + energy_range + "/" + root_file + "           output directory" + os.linesep)
    file.write("DATBAS  F                             write .dbase file" + os.linesep)
    file.write("USER    oscar                         user" + os.linesep)
    file.write("DEBUG   F 6 F 1000000                 debug flag and log.unit for out" + os.linesep)
    file.write("EXIT")
    file.close()
    seed1 = seed1 + 2
    seed2 = seed2 + 2
    seed3 = seed3 + 2    

for i in range(len(run_num)):
    file = open(work_dir + "/SBATCH_" + card_name + "_" + str(i+1).zfill(3) + ".sh", "w")
    file.write("#!/bin/bash" + os.linesep)
    file.write("#SBATCH --account=rrg-mdiamond"  + os.linesep)
    file.write("#SBATCH --job-name=corsika" + str(prmpar) + os.linesep)
    file.write("#SBATCH --output=corsika-%J.out" + os.linesep)
    file.write("#SBATCH " + time_cpu + os.linesep)
    file.write("#SBATCH --ntasks=1" + os.linesep)
    file.write("#SBATCH --mem-per-cpu=2G" + os.linesep)
    file.write(""  + os.linesep)
    file.write("module load gcc/8.3.0" + os.linesep)
    file.write("export FLUPRO=/home/oscargmo/MathuslaCR/Fluka/Fluka2020" + os.linesep)
    file.write("export FLUFOR=gfortran" + os.linesep)
    file.write("export F77=gfortran" + os.linesep)
    file.write("cd  " + work_dir + os.linesep)
    file.write("## CORSIKA execution" + os.linesep)
    file.write(ejecutable + card_name + "_" + str(i+1).zfill(3) + ".input > " + work_dir + energy_range + "/" + card_name + "_" + str(i+1).zfill(3) + ".out")
    file.close()

for i in range(len(run_num)):
    file = open(work_dir + energy_range + "/CSK2ROOT_" + card_name + "_" + str(i+1).zfill(3) + ".sh", "w")
    file.write("#!/bin/bash" + os.linesep)
    file.write("#SBATCH --account=rrg-mdiamond"  + os.linesep)
    file.write("#SBATCH --job-name=csk2root" + str(prmpar) + os.linesep)
    file.write("#SBATCH --output=csk2root" + primario + "%J.out" + os.linesep)
    file.write("#SBATCH " + time_csk2root + os.linesep)
    file.write("#SBATCH --ntasks=1" + os.linesep)
    file.write("#SBATCH --mem-per-cpu=24G" + os.linesep)
    file.write(""  + os.linesep)
    file.write("module load root" + os.linesep)
    file.write("export COAST_DIR=/home/oscargmo/MathuslaCR/Coast/coast-v3r3" + os.linesep)
    file.write("export LD_LIBRARY_PATH=$COAST_DIR/lib:$LD_LIBRARY_PATH" + os.linesep)
    file.write("export PATH=$COAST_DIR/CorsikaToROOT:$PATH" + os.linesep)
    file.write("cd  " + work_dir + energy_range + os.linesep)
    file.write("## corsika2root execution" + os.linesep)
    file.write("corsika2root " + root_file + "DAT" + str(i+1).zfill(6))
    file.close()

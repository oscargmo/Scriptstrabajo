# -*- coding: utf-8 -*-
import numpy as np
import os

# Directorio de trabajo
work_dir = str(os.getcwd()) + "/"
print("\nDirectorio actual:" + work_dir)
# Construcción de la ruta hacia los datos
almacen_general = "/home/oscargmo/scratch/mathustaCR/"
# Modelos hadronicos: EPOS-LHC, QGSJET-II-04, SIBYLL2.3c
HI_model  = "EPOS-LHC"
tipo_angular = "vertical"
primario = "Fe" #RC primario
prefix_root_file = "Z=26_A=56_NSHOW=1_" #prefijo de las simulaciones CORSIKA
energy_range = "10000-100000TeV"  # Rango de energía y rango azimutal
time_to_nalyze = "--time=36:00:00" # Tiempo requerido para analizar las cascadas 
mem_request = "--mem-per-cpu=8G" # Memoria RAM usada para el ananlisis
# Nombre del archivos.dat que se va a crear 
name_data_file = "MC-" + primario + "-" + HI_model + "_E_" + energy_range + ".dat"
macro_JC = "Signals_MathuslaArgo_EAS_Reco_" + tipo_angular + "_v8_" + primario + ".C"

# Verificamos que exista el directorio con los datos
dir_csk_files = almacen_general + HI_model + "/" + tipo_angular + "/corsika-77100/run/" + energy_range + "/root_files"
if os.path.isdir(dir_csk_files):
    print("\nEste es el directorio de donde se tomaran los datos:" + dir_csk_files)
else:
    print("\nNO existe el directorio!!, verifica la ruta:" + dir_csk_files)
        
run_number = []
for i in range(150):
    run_number.append(i + 1)
    os.system("mkdir -p " + work_dir + primario + "_JOBID" + str(i+1).zfill(3))

print(run_number)

for i in range(len(run_number)):
    file = open(work_dir + primario +"_JOBID" + str(i+1).zfill(3) + "/" + name_data_file, "w") 
    if os.path.isfile(dir_csk_files + "/" + prefix_root_file + "DAT" + str(i+1).zfill(6) + ".root"):
        print("Se analizara el archivo: " + prefix_root_file + "DAT" + str(i+1).zfill(6) + ".root")
    else:
        print("NO existe el archivo: " + prefix_root_file + "DAT" + str(i+1).zfill(6) + ".root")
    file.write(dir_csk_files + "/" + prefix_root_file + "DAT" + str(i+1).zfill(6) + ".root" + os.linesep)
    file.close()

##### Ahora creamos los .SBATCH para someter los trabajos al cluster (LARCAD)
for i in range(len(run_number)):
    file = open(work_dir + primario + "_JOBID" + str(i+1).zfill(3) + "/SBATCH_" + primario + "_" + str(i+1).zfill(3) + ".sh", "w")
    file.write("#!/bin/bash" + os.linesep)
    file.write(""  + os.linesep)
    file.write("#SBATCH --account=rrg-mdiamond" + os.linesep)
    file.write("#SBATCH --job-name=analisis"+ primario  + os.linesep)
    file.write("#SBATCH --output=analisis"+ primario +"-%J.out " + os.linesep)
    file.write("#SBATCH " + time_to_nalyze + os.linesep)
    file.write("#SBATCH --ntasks=1 " + os.linesep)
    file.write("#SBATCH "+ mem_request + os.linesep)
    file.write("## Copiamos la macro de JC al directorio de trabajo" + os.linesep)
    file.write("cp " +  work_dir + macro_JC + " " + work_dir + primario + "_JOBID" + str(i+1).zfill(3) + "/" + os.linesep)
    file.write("## Nos movemos al directorio de trabajo"+ os.linesep)
    file.write("cd  " + work_dir + primario + "_JOBID" + str(i+1).zfill(3)  + os.linesep)
    file.write("module load root" + os.linesep)
    file.write("" + os.linesep)
    file.write("## Ejecutamos ROOT" + os.linesep)
    file.write("root.exe -q -l -b " + macro_JC)
    file.close()

if not os.path.isfile(work_dir + macro_JC):
        print("\n¡¡¡ OJO !!! Tienes que copiar " + macro_JC + " en la carpeta " + work_dir)

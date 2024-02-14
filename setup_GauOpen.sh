#!/bin/bash -e

# ====================================
# Load python and gcc modules (This is specifically for Rapoi VUW computer cluster)
module load GCCcore/10.3.0
module load GCC/10.3.0
module load Python/3.9.5

# ====================================
# Download GauOpen v2
rm -fr gauopen_v2
mkdir -p gauopen_v2
cd gauopen_v2
curl https://gaussian.com/g16/gauopen_v2.zip -o gauopen_v2.zip
unzip gauopen_v2.zip

# ====================================
# Remove any compiled programs
make -f qc.make clean
make -f qc.make clean
rm -fr domp2 readmat readmat8 writemat writemat8 *.f *.so *.o *.mat *.dat *.log __pycache__

# ====================================
# Compile the program
make -f qc.make all

# ====================================
# Convert name of so file to qcmatrixio.so
mv qcmatrixio.cpython*.so qcmatrixio.so

# ====================================
# Move back into original path
cd ..

#!/bin/bash -e
#SBATCH --job-name=RGME_Water-DFT
#SBATCH --cpus-per-task=1
#SBATCH --mem=256GB
#SBATCH --partition=bigmem
#SBATCH --constraint=AVX
#SBATCH --time=10-00:00     # Walltime
#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID
#SBATCH --error=slurm-%j.err

# ----------------------------

#module load Python/3.9.5

module load GCCcore/5.4.0
module load GCC/5.4.0
module load python/3.6.8

get_gaussian_matrix_elements.py matrix_data.dat

# ----------------------------
echo "End of job"
# ----------------------------

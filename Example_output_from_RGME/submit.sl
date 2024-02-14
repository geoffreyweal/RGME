#!/bin/bash -e
#SBATCH --job-name=water_example
#SBATCH --cpus-per-task=16
#SBATCH --mem=64GB
#SBATCH --partition=parallel
#SBATCH --constraint=AVX
#SBATCH --time=1-00:00     # Walltime
#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID
#SBATCH --error=slurm-%j.err

# ----------------------------
# Load Gaussian

module load gaussian/g16

# ----------------------------
# Perform Gaussian Calculation

srun g16 < water.gjf > water.log

# ----------------------------
# Remove temp files

#rm -fvr checkpoint.chk

# ----------------------------
echo "End of job"
# ----------------------------

# The Read Gaussian Matrix Elements (RGME) Program

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/geoffreyweal/RGME)](https://github.com/geoffreyweal/RGME)
[![Licence](https://img.shields.io/github/license/geoffreyweal/RGME)](https://www.gnu.org/licenses/agpl-3.0.en.html)

Authors: Dr. Geoffrey Weal<sup>\*</sup>, Dr. Paul Hume<sup>\*</sup>, Prof. Justin Hodgkiss<sup>\*</sup>

<sup>\*</sup> Victoria University of Wellington, Wellington, New Zealand; The MacDiarmid Institute for Advanced Materials and Nanotechnology, Wellington, New Zealand. 

Group pages: https://people.wgtn.ac.nz/paul.hume/grants, https://people.wgtn.ac.nz/justin.hodgkiss/grants

## What is the Read Gaussian Matrix Elements (RGME) Program

This program is designed to set up the Gaussian-built programs for extracting data from Gaussian Quantum Chemistry Software using the ``output=(MatrixElement)`` command in the ``.gjf`` file, and then convert the matrices into csv files for further analysis by the user. 

## Installation

This program requires Fortran and Python3 to run.

To install this program, perform the following in your terminal

1. Change directory into the directory that you want to place this program in.
2. Type into the terminal ``git clone https://github.com/geoffreyweal/RGME.git``. This will download the RGME program into the current directory.
3. Type into the terminal ``chmod -R 777 RGME``. This will change the permissions of this program so that your computer can run this program.
3. Type into the terminal ``echo 'export PATH='"$PWD"'/RGME:$PATH' >> ~/.bashrc``. This will allow you computer to know where the files to run are located.
4. Type into the terminal ``source ~/.bashrc``. This will refresh your terminal so it recognises this program.
5. Change directory into the RGME folder: ``cd RGME``
6. Run the bash script called ``setup_GauOpen.sh``: ``bash setup_GauOpen.sh``. This will download the ``gauopen_v2`` program from Gaussian and compile the ``readmat8`` Gaussian program. This ``readmat8`` program is used by RGME. See below for more information about this script. 

### The ``setup_GauOpen.sh`` script

This script will download the Gaussian Interfacing program ``gauopen_v2.zip`` and compile the program. This will create the ``readmat8`` program that is used by RGME.

#### Note: 

The start of this program include ``module load`` commands that will load the Fortran compiler and Python. 

```bash
module load gcc/8.2.0
module load python/3.7.3
```

This is commonly used in computer clusters like those that use the ``SLURM`` scheduler. If you dont need to include these, remove them from your ``setup_GauOpen.sh`` script. If you are installing this program on your local or personal computer, you probably dont need these, and these lines can be removed. 

The Fortran compiler used in this example is GCC. Change this to your Fortran compiler if needed.

## How To Use This Program

### 1: Run Gaussian

Run your Gaussian job as you usually would. Include in the Gaussian input file the input ``output=(MatrixElement)
``. At the bottom of your file, include the name of the file you want Gaussian to place the matrix data you desire into. **This is the recommended way**

An example Gaussian input file is given below:

```
%chk=checkpoint.chk
%nprocshared=16
%mem=60GB
# wB97XD/6-31+G(d,p) ! ASE formatted method and basis
# nosymm ! 
# Int=UltraFine ! This is default in G16, but here if calcs are run on other Gaussian. This splits the intergration grid into very tiny pieces (99,590 grid points).
# maxdisk=2TB scf=(xqc,maxcycle=512)
# output=(MatrixElement)

Gaussian input prepared by ASE: Reorganisation Energy Job

0 1
O		1.80172602 		0.06746038 		0.00000000
H		2.76172599 		0.06770148 		0.00000000
H		1.48149872		0.97247667 		0.00000000

matrix_data.dat


```

You can also use the checkpoint file to gather this information. An example Gaussian input file is given below:

```
%oldchk=oldcheckpoint.chk
%chk=checkpoint.chk
%nprocshared=16
%mem=60GB
# wB97XD/6-31+G(d,p) ! ASE formatted method and basis
# nosymm ! 
# Int=UltraFine ! This is default in G16, but here if calcs are run on other Gaussian. This splits the intergration grid into very tiny pieces (99,590 grid points).
# maxdisk=2TB scf=(xqc,maxcycle=512)
# density(check) geom=check 
# output=(MatrixElement)

Gaussian input prepared by ASE: Reorganisation Energy Job

0 1

matrix_data.dat


```

### 2: Run the RGME program

Run the RGME program in the terminal. Do this by running the following command in te terminal:

``` bash
get_gaussian_matrix_elements.py matrix_data.dat
```

where ``matrix_data.txt`` is the file that the matrix data from Gaussian was recorded into.

### 3: You Have Your Data

You will now see that there is a new folder called ``MatrixElementsFiles``. This folder will create a number of csv files that contain the matrix data that could be obtained from the ``matrix_data.txt`` file. 

### 4. Check the Data in ``MatrixElementsFiles`` Makes Sense

This is still a new program and files may not be created properly. Where possible, check however you can that the data make sense to you. If it doesn't, create an issue in the Github Issues Page for this program and write the problem(s) you have in here: https://github.com/geoffreyweal/RGME/issues

## Useful Gaussian ``.gjf`` Inputs

* You want to obtain the quadrupole, octupole, or hexadecapole integral matrices for your system (https://gaussian.com/overlay3/#iop_(3/36)): 
	* Quadrupole: Include ``IOp(3/36=2)`` in your Gaussian ``.gjf`` file.
	* Octupole: Include ``IOp(3/36=3)`` in your Gaussian ``.gjf`` file.
	* Hexadecapole: Include ``IOp(3/36=4)`` in your Gaussian ``.gjf`` file.

## Issues

This program is definitely a "work in progress". I have made it as easy to use as possible, but there are always oversights to program development and some parts of it may not be as easy to use as it could be. If you have any issues with the program or you think there would be better/easier ways to use and implement things in RGME, create a notice in the Github Issues section. Feedback is very much welcome!

Issues: https://github.com/geoffreyweal/RGME/issues

## About

<div align="center">

| Repositories | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/geoffreyweal/RGME)](https://github.com/geoffreyweal/RGME) |
|:----------------------:|:-------------------------------------------------------------:|
| License | [![Licence](https://img.shields.io/github/license/geoffreyweal/RGME)](https://www.gnu.org/licenses/agpl-3.0.en.html) |
| Authors | Dr. Geoffrey Weal, Dr. Paul Hume, Prof. Justin Hodgkiss |
| Group Websites | https://people.wgtn.ac.nz/paul.hume/grants, https://people.wgtn.ac.nz/justin.hodgkiss/grants |

</div>

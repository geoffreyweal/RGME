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

#### Note 1: 

The start of ``setup_GauOpen.sh`` script includes ``module load`` commands that will load the Fortran compiler and Python. 

```bash
module load GCCcore/5.4.0
module load GCC/5.4.0
module load python/3.6.8
```

This is commonly used in computer clusters like those that use the ``SLURM`` scheduler. If you dont need to include these, remove them from your ``setup_GauOpen.sh`` script. If you are installing this program on your local or personal computer, you probably dont need these, and these lines can be removed. 

The Fortran compiler used in this example is GCC. Change this to your Fortran compiler if needed.

#### Note 2: 

It seems to be important that you use the same version of GCC and Python to setup and run the RGME program. I.e, if you use GCC/5.4.0 and python/3.6.8 to setup us the RGME program, make sure you also load these versions of python and GCC before running the RGME (``get_gaussian_matrix_elements.py``) program. 

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

If you are submitting this job with slurm, here is an example ``submit.sl`` file you can use to submit the Gaussian job to slurm (you may need to modify it to use on your slurm system)

```
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
```

### 2: Run the RGME program

Run the RGME program in the terminal. Do this by running the following command in the terminal:

``` bash
get_gaussian_matrix_elements.py matrix_data.dat
```

where ``matrix_data.txt`` is the file that the matrix data from Gaussian was recorded into.


---
**NOTE**

If you have any problems when running this step, try changing the version of GCC and python that you used when running the ``setup_GauOpen.sh`` script. You can check what version you used by looking at your ``setup_GauOpen.sh`` file in a text file. For me this was: 

```bash
module load GCCcore/5.4.0
module load GCC/5.4.0
module load python/3.6.8
```

---


### 3: You Have Your Data

You will now see that there is a new folder called ``MatrixElementsFiles``. This folder will create a number of csv files that contain the matrix data that could be obtained from the ``matrix_data.txt`` file. 

### 4. Check the Data in ``MatrixElementsFiles`` Makes Sense

This is still a new program and files may not be created properly. Where possible, check however you can that the data make sense to you. If it doesn't, create an issue in the Github Issues Page for this program and write the problem(s) you have in here: https://github.com/geoffreyweal/RGME/issues

## Useful Gaussian ``.gjf`` Inputs

* You want to obtain the quadrupole, octupole, or hexadecapole integral matrices for your system (https://gaussian.com/overlay3/#iop_(3/36)): 
	* Quadrupole: Include ``IOp(3/36=2)`` in your Gaussian ``.gjf`` file.
	* Octupole: Include ``IOp(3/36=3)`` in your Gaussian ``.gjf`` file.
	* Hexadecapole: Include ``IOp(3/36=4)`` in your Gaussian ``.gjf`` file.

## Troubleshooting

1. Check that you are able to download and unzip the gauopen_v2.zip program from Gaussian. If you can't do this, you will not be able to run the ``setup_GauOpen.sh`` script during installation. 

```
curl https://gaussian.com/g16/gauopen_v2.zip -o gauopen_v2.zip
unzip gauopen_v2.zip
```

## Known issues

### During setup I get the error --> ```assert parents[-3][0] == 'vars': AssertionError```

When setting up the ``bash setup_GauOpen.sh`` script. I get something like the following error:

```
Traceback (most recent call last):
  File "/nfs/home/username/.local/bin/f2py3", line 8, in <module>
    sys.exit(main())
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/f2py2e.py", line 702, in main
    run_compile()
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/f2py2e.py", line 669, in run_compile
    setup(ext_modules=[ext])
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/distutils/core.py", line 169, in setup
    return old_setup(**new_attr)
  File "/home/software/apps/python/3.8.1/lib/python3.8/distutils/core.py", line 148, in setup
    dist.run_commands()
  File "/home/software/apps/python/3.8.1/lib/python3.8/distutils/dist.py", line 966, in run_commands
    self.run_command(cmd)
  File "/home/software/apps/python/3.8.1/lib/python3.8/distutils/dist.py", line 985, in run_command
    cmd_obj.run()
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/distutils/command/build.py", line 62, in run
    old_build.run(self)
  File "/home/software/apps/python/3.8.1/lib/python3.8/distutils/command/build.py", line 135, in run
    self.run_command(cmd_name)
  File "/home/software/apps/python/3.8.1/lib/python3.8/distutils/cmd.py", line 313, in run_command
    self.distribution.run_command(command)
  File "/home/software/apps/python/3.8.1/lib/python3.8/distutils/dist.py", line 985, in run_command
    cmd_obj.run()
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/distutils/command/build_src.py", line 144, in run
    self.build_sources()
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/distutils/command/build_src.py", line 161, in build_sources
    self.build_extension_sources(ext)
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/distutils/command/build_src.py", line 321, in build_extension_sources
    sources = self.f2py_sources(sources, ext)
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/distutils/command/build_src.py", line 562, in f2py_sources
    numpy.f2py.run_main(f2py_options + ['--lower',
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/f2py2e.py", line 441, in run_main
    postlist = callcrackfortran(files, options)
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/f2py2e.py", line 342, in callcrackfortran
    postlist = crackfortran.crackfortran(files)
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3316, in crackfortran
    postlist = traverse(postlist, hook)
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3388, in traverse
    new_index, new_item = traverse((index, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3396, in traverse
    new_key, new_value = traverse((key, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3388, in traverse
    new_index, new_item = traverse((index, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3396, in traverse
    new_key, new_value = traverse((key, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3388, in traverse
    new_index, new_item = traverse((index, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3396, in traverse
    new_key, new_value = traverse((key, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3396, in traverse
    new_key, new_value = traverse((key, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3396, in traverse
    new_key, new_value = traverse((key, value), visit,
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3375, in traverse
    new_result = visit(obj, parents, result, *args, **kwargs)
  File "/nfs/home/username/.local/lib/python3.8/site-packages/numpy/f2py/crackfortran.py", line 3434, in character_backward_compatibility_hook
    assert parents[-3][0] == 'vars'
AssertionError
make: *** [qc.make:31: qcmatrixio.cpython-34m.so] Error 1
```

**Potential Solution**: This seems to be caused by using a too modern version of fortran compiler (GCC) and python. Here, you can see that Python 3.8.1 was used by f2py3. As you can see in the top part of the error message above: 

```
Traceback (most recent call last):
  File "/nfs/home/username/.local/bin/f2py3", line 8, in <module>
    sys.exit(main())
```

This is what the ```f2py3``` program looked like for this run

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
from numpy.f2py.f2py2e import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

NOTE: for some people the first line of this program might be different. For example, rather than ```#!/usr/bin/python3```, the first line might be ```#!/home/software/apps/python/3.8.1/bin/python3.8```. 

Try changing this to ```#!/usr/bin/env python3``` and run your program with Python 3.6 (or Python 3.6.8) and rerun the `bash setup_GauOpen.sh`` script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from numpy.f2py.f2py2e import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```


### During setup (``bash setup_GauOpen.sh``) I get the error --> ```/usr/bin/python3: symbol lookup error: /usr/bin/python3: undefined symbol: _Py_LegacyLocaleDetected```

This also seems to be due to running invalid versions of Python and GCC. Try using older versions of these programs, and check the ```f2py3``` program, and potentially change the first line from ``#!/usr/bin/python3`` to ``#!/usr/bin/env python3``:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from numpy.f2py.f2py2e import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

Older version of Python and GCC that worked for me are:

```bash
module load GCCcore/5.4.0
module load GCC/5.4.0
module load python/3.6.8
```


### During running ```get_gaussian_matrix_elements.py``` I see the error --> error while loading shared libraries: libgfortran.so.3: cannot open shared object file: No such file or directory

This is likely because you are using an invalid version of Python and GCC. Try using the same version you used for setting up the ``bash setup_GauOpen.sh``. This problem seems to be particularly affected by the version of GCC and GCCcore you used during the ``bash setup_GauOpen.sh`` step, however your choice of python can also change the version of GCC and GCCcore that you used. Check what versions of GCC, GCCcore, and Python you used after installation of ``bash setup_GauOpen.sh`` by running the command below after running the ``bash setup_GauOpen.sh`` step:

```bash
module list
```

For me I used the following:

```bash
module load GCCcore/5.4.0
module load GCC/5.4.0
module load python/3.6.8
```


## Do you have new issues

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

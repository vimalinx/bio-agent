# kinfold Help Reference

- Command: `Kinfold`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/Kinfold`
- Summary: CLI installed by bioconda package viennarna.
- Package names: viennarna

## Captured Version

```text
$ Kinfold --version
Kinfold 1.4
```

## Captured Help

```text
$ Kinfold --help
Usage: Kinfold [OPTION]...
Stochastic Folding Simulations of Single-Stranded Nucleic Acids

  -h, --help            Print help and exit
      --full-help       Print help, including hidden options, and exit
  -V, --version         Print version and exit

Energy Model:
  -d, --dangle=INT      <0|1|2> set dangling end model to (none|normal|double)
                          (possible values="0", "1", "2" default=`2')
  -T, --Temp=FLOAT      simulation temperature  (default=`37')
  -P, --Par=filename    read energy-parameter-file
      --logML           use logarithmic multiloop energies instead of linear
                          (default=on)

MoveSet:
      --noShift         turn off shift-moves  (default=off)
      --noLP            forbid structures with isolated base-pairs
                          (default=off)

Simulation:
      --seed=STRING     set random number seed specify 3 integers as
                          int=int=int  (default=`clock')
      --time=FLOAT      set maxtime of simulation  (default=`500')
      --num=INT         set number of trajectories  (default=`1')
      --start           read start structure from stdin (otherwise use open
                          chain)  (default=off)
      --stop            read stop structure(s) from stdin (otherwise use MFE)
                          (default=off)
      --met             use Metropolis rule for rates (not Kawasaki rule)
                          (default=off)
      --fpt             compute first passage time (stop when a stop-structure
                          is reached)  (default=on)
      --rect            compute recurrence time (of a start structure which is
                          contained in stop structures)  (default=off)
      --grow=FLOAT      grow chain every <float> time units  (default=`0')
      --glen=INT        initial size of growing chain  (default=`15')

Output:
      --log=filename    set basename of log-file  (default=`kinout')
  -q, --silent          no output to stdout  (default=off)
  -v, --verbose         more information to stdout  (default=off)
      --lmin            output only local minima to stdout  (default=off)
      --cut=FLOAT       only print structures with E <= MFE + <float> to stdout
                          (default=`20')
Input File Format:
  1st line sequence
  2nd line start structure (if option --start is used)
  following lines are stop structures (if option --stop is used)
```

## Captured Man Page

```text
No man page captured.
```

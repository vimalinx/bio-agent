# cleanup-blastdb-volumes-py Help Reference

- Command: `cleanup-blastdb-volumes.py`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/cleanup-blastdb-volumes.py`
- Summary: CLI installed by bioconda package blast.
- Package names: blast

## Captured Version

```text
$ cleanup-blastdb-volumes.py --version
usage: cleanup-blastdb-volumes.py [-h] -db DB -dbtype {prot,nucl} [-dry-run]
                                  [-version] [-verbose]
cleanup-blastdb-volumes.py: error: the following arguments are required: -db, -dbtype
```

## Captured Help

```text
$ cleanup-blastdb-volumes.py --help
usage: cleanup-blastdb-volumes.py [-h] -db DB -dbtype {prot,nucl} [-dry-run]
                                  [-version] [-verbose]

Remove needless BLAST database volumes.

options:
  -h, --help           show this help message and exit
  -db DB               BLAST database name
  -dbtype {prot,nucl}  Molecule type
  -dry-run             Do not delete any files, just list them
  -version             show program's version number and exit
  -verbose             Increase output verbosity
```

## Captured Man Page

```text
No man page captured.
```

# efilter Help Reference

- Command: `efilter`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/efilter`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ efilter --version
ERROR:  Unrecognized option --version
```

## Captured Help

```text
$ efilter --help
efilter 24.0

Query Specification

  -query       Query string

Date Constraint

  -days        Number of days in the past
  -datetype    Date field abbreviation
  -mindate     Start of date range
  -maxdate     End of date range

Overview

  All efilter shortcuts can also be used with esearch

  Each shortcut is only legal for a specific database category

Publication Filters

  -pub         abstract, clinical, english, free, historical,
               journal, medline, preprint, published, retracted,
               retraction, review, structured
  -journal     pnas, "j bacteriol", ...
  -released    last_week, last_month, last_year, prev_years

Sequence Filters

  -country     usa:minnesota, united_kingdom, "pacific ocean", ...
  -feature     gene, mrna, cds, mat_peptide, ...
  -location    mitochondrion, chloroplast, plasmid, plastid
  -molecule    genomic, mrna, trna, rrna, ncrna
  -organism    animals, archaea, bacteria, eukaryotes, fungi,
               human, insects, mammals, plants, prokaryotes,
               protists, rodents, viruses
  -source      genbank, insd, pdb, pir, refseq, select, swissprot,
               tpa
  -division    bct, con, env, est, gss, htc, htg, inv, mam, pat,
               phg, pln, pri, rod, sts, syn, una, vrl, vrt
  -keyword     purpose
  -purpose     baseline, targeted

Gene Filters

  -status      alive
  -type        coding, pseudo

SNP Filters

  -class       acceptor, donor, coding, frameshift, indel,
               intron, missense, nonsense, synonymous

Assembly Filters

  -status      latest, replaced

Examples

  esearch -db pubmed -query "opsin gene conversion" |
  elink -related |
  efilter -query "tetrachromacy"

  esearch -db pubmed -query "opsin gene conversion" |
  efilter -mindate 2015


curl: (56) response reading failed (errno: 115)
 ERROR:  curl command failed ( Fri Mar 27 12:10:14 CST 2026 ) with: 56
ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/versions/
/home/vimalinx/miniforge3/envs/bio/bin/ecommon.sh: line 1628: [: : integer expected
/home/vimalinx/miniforge3/envs/bio/bin/ecommon.sh: line 1631: [: : integer expected
```

## Captured Man Page

```text
No man page captured.
```

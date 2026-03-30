# esummary Help Reference

- Command: `esummary`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/esummary`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ esummary --version
ERROR:  Unrecognized option --version
```

## Captured Help

```text
$ esummary --help
esummary 24.0

Mode Selection

  -mode          xml, json

Direct Record Selection

  -db            Database name
  -id            Unique identifier or accession number
  -input         Read identifier(s) from file instead of stdin

Miscellaneous

  -raw           Skip database-specific XML modifications

Accession Mapping Examples

  esummary -db annotinfo -id GCF_000001405.31

  esummary -db assembly -id 202921,GCF_000001405.38

  esummary -db bioproject -id PRJNA257197

  esummary -db biosample -id SAMN03737421

  esummary -db books -id NBK2261

  esummary -db cdd -id TIGR03462

  esummary -db clinvar -id VCV000010510

  esummary -db dbvar -id esv1921070

  esummary -db gds -id GSE22309

  esummary -db genome -id PRJNA9559

  esummary -db geoprofiles -id AW295812

  esummary -db gtr -id GTR000559277

  esummary -db ipg -id NP_001234226.1

  esummary -db medgen -id C0000744

  esummary -db mesh -id D007328

  esummary -db pcsubstance -id D061267

  esummary -db proteinclusters -id PLN03776

  esummary -db seqannot -id NA000008723.1

  esummary -db sra -id SRR5437876


curl: (56) response reading failed (errno: 115)
 ERROR:  curl command failed ( Fri Mar 27 12:22:11 CST 2026 ) with: 56
ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/versions/
/home/vimalinx/miniforge3/envs/bio/bin/ecommon.sh: line 1628: [: : integer expected
/home/vimalinx/miniforge3/envs/bio/bin/ecommon.sh: line 1631: [: : integer expected
```

## Captured Man Page

```text
No man page captured.
```

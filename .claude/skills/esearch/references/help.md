# esearch Help Reference

- Command: `esearch`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/esearch`
- Summary: CLI installed by bioconda package entrez-direct.
- Package names: entrez-direct

## Captured Version

```text
$ esearch --version
ERROR:  Unrecognized option --version
```

## Captured Help

```text
$ esearch --help
esearch 24.0

Query Specification

  -db            Database name
  -query         Query string

Spell Check

  -spell         Correct misspellings in query

Query Translation

  -translate     Show automatic term mapping
  -component     Individual term mapping items

Document Order

  -sort          Result presentation order

Sort Choices by Database

  gene           Chromosome, Gene Weight, Name, Relevance

  geoprofiles    Default Order, Deviation, Mean Value, Outliers, Subgroup Effect

  pubmed         First Author, Journal, Last Author, Pub Date, Recently Added,
                 Relevance, Title

  (sequences)    Accession, Date Modified, Date Released, Default Order,
                 Organism Name, Taxonomy ID

  snp            Chromosome Base Position, Default Order, Heterozygosity,
                 Organism, SNP_ID, Success Rate

Note

  All efilter shortcuts can also be used with esearch

Examples

  esearch -db pubmed -query "opsin gene conversion OR tetrachromacy"

  esearch -db pubmed -query "Garber ED [AUTH] AND PNAS [JOUR]"

  esearch -db nuccore -query "MatK [GENE] AND NC_0:NC_999999999 [PACC]"

  esearch -db protein -query "amyloid* [PROT]" |
  elink -target pubmed -label prot_cit |
  esearch -db gene -query "apo* [GENE]" |
  elink -target pubmed -label gene_cit |
  esearch -query "(#prot_cit) AND (#gene_cit)" |
  efetch -format docsum |
  xtract -pattern DocumentSummary -element Id Title


curl: (56) response reading failed (errno: 115)
 ERROR:  curl command failed ( Fri Mar 27 12:12:30 CST 2026 ) with: 56
ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/versions/
/home/vimalinx/miniforge3/envs/bio/bin/ecommon.sh: line 1628: [: : integer expected
/home/vimalinx/miniforge3/envs/bio/bin/ecommon.sh: line 1631: [: : integer expected
```

## Captured Man Page

```text
No man page captured.
```

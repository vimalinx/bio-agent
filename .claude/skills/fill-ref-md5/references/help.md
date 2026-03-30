# fill-ref-md5 Help Reference

- Command: `fill-ref-md5`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/fill-ref-md5`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ fill-ref-md5 --version
Unknown parameter "--version" or non-existent file. Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/fill-ref-md5 line 19.
	main::error("Unknown parameter \"--version\" or non-existent file. Run -h fo"...) called at /home/vimalinx/miniforge3/envs/bio/bin/fill-ref-md5 line 48
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/fill-ref-md5 line 9
```

## Captured Help

```text
$ fill-ref-md5 --help
About: The script computes MD5 sum of the reference sequence and inserts
   'reference' and 'contig' tags into header as recommended by VCFv4.1.
   The VCF file must be compressed and tabix indexed, as it takes advantage
   of the lightning fast tabix reheader functionality.
Usage: fill-ref-md5 [OPTIONS] in.vcf.gz out.vcf.gz
Options:
   -d, --dictionary <file>             Where to read/write computed MD5s. Opened in append mode, existing records are not touched.
   -i, --info <AS:xx,SP:xx,TX:xx>      Optional info on reference assembly (AS), species (SP), taxonomy (TX)
   -r, --refseq <file>                 The reference sequence in fasta format indexed by samtools faidx
   -h, -?, --help                      This help message.
Examples:
   fill-ref-md5 -i AS:NCBIM37,SP:"Mus\ Musculus" -r NCBIM37_um.fa  -d NCBIM37_um.fa.dict in.vcf.gz out.vcf.gz
```

## Captured Man Page

```text
No man page captured.
```

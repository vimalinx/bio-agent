# vcf-convert Help Reference

- Command: `vcf-convert`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-convert`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-convert --version
Use of uninitialized value in numeric lt (<) at /home/vimalinx/miniforge3/envs/bio/bin/vcf-convert line 60.
Downgrading of VCF versions is experimental: expect troubles!
Broken VCF header, no column names?
 at /home/vimalinx/miniforge3/envs/bio/lib/perl5/site_perl/Vcf.pm line 172.
	Vcf::throw(Vcf4_2=HASH(0x55dac3d0a928), "Broken VCF header, no column names?") called at /home/vimalinx/miniforge3/envs/bio/lib/perl5/site_perl/Vcf.pm line 867
	VcfReader::_read_column_names(Vcf4_2=HASH(0x55dac3d0a928)) called at /home/vimalinx/miniforge3/envs/bio/lib/perl5/site_perl/Vcf.pm line 602
	VcfReader::parse_header(Vcf4_2=HASH(0x55dac3d0a928)) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-convert line 63
	main::convert_file(HASH(0x55dac3cce248)) called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-convert line 12
```

## Captured Help

```text
$ vcf-convert --help
About: Convert between VCF versions.
Usage: cat in.vcf | vcf-convert [OPTIONS] > out.vcf
Options:
   -r, --refseq <file>              The reference sequence in samtools faindexed fasta file. (Not required with SNPs only.)
   -v, --version <string>           4.0, 4.1, 4.2
   -h, -?, --help                   This help message.
```

## Captured Man Page

```text
No man page captured.
```

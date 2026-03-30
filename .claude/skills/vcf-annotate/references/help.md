# vcf-annotate Help Reference

- Command: `vcf-annotate`
- Sources: conda_bioconda
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-annotate`
- Summary: CLI installed by bioconda package vcftools.
- Package names: vcftools

## Captured Version

```text
$ vcf-annotate --version
Unknown parameter "--version". Run -h for help.
 at /home/vimalinx/miniforge3/envs/bio/bin/vcf-annotate line 42.
	main::error("Unknown parameter \"--version\". Run -h for help.\x{a}") called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-annotate line 159
	main::parse_params() called at /home/vimalinx/miniforge3/envs/bio/bin/vcf-annotate line 32
```

## Captured Help

```text
$ vcf-annotate --help
About: Annotates VCF file, adding filters or custom annotations. Requires tabix indexed file with annotations.
   Currently it can annotate ID, QUAL, FILTER and INFO columns, but will be extended on popular demand.
   For examples of user-defined filters see online documentation or examples/filters.txt in vcftools distribution.
Usage: cat in.vcf | vcf-annotate [OPTIONS] > out.vcf
Options:
   -a, --annotations <file.gz>         The tabix indexed file with the annotations: CHR\tFROM[\tTO][\tVALUE]+.
   -c, --columns <list>                The list of columns in the annotation file, e.g. CHROM,FROM,TO,-,QUAL,INFO/STR,INFO/GN. The dash
                                           in this example indicates that the third column should be ignored. If TO is not
                                           present, it is assumed that TO equals to FROM. When REF and ALT columns are present, only
                                           matching lines are annotated.
   -d, --description <file|string>     Header annotation, e.g. key=INFO,ID=HM2,Number=0,Type=Flag,Description='HapMap2 membership'.
                                           The descriptions can be read from a file, one annotation per line.
       --fill-AC-AN                    (Re)Calculate AC and AN tags
       --fill-HWE                      (Re)Calculate HWE, AC and AN tags
       --fill-ICF                      (Re)Calculate Inbreeding Coefficient F, HWE, AC and AN
       --fill-type                     Annotate INFO/TYPE with snp,del,ins,mnp,complex
   -f, --filter <file|list>            Apply filters, list is in the format flt1=value/flt2/flt3=value/etc. If argument to -f is a file,
                                           user-defined filters be applied. See User Defined Filters below.
   -H, --hard-filter                   Remove lines with FILTER anything else than PASS or "."
   -n, --normalize-alleles             Make REF and ALT alleles more compact if possible (e.g. TA,TAA -> T,TA).
   -r, --remove <list>                 Comma-separated list of tags to be removed (e.g. ID,INFO/DP,FORMAT/DP,FILTER).
   -h, -?, --help                      This help message.
Filters:
	+                           		Apply all filters with default values (can be overriden, see the example below).
	-X                          		Exclude the filter X
	1, StrandBias  FLOAT        		Min P-value for strand bias (INFO/PV4) [0.0001]
	2, BaseQualBias  FLOAT      		Min P-value for baseQ bias (INFO/PV4) [0]
	3, MapQualBias  FLOAT       		Min P-value for mapQ bias (INFO/PV4) [0]
	4, EndDistBias  FLOAT       		Min P-value for end distance bias (INFO/PV4) [0.0001]
	a, MinAB  INT               		Minimum number of alternate bases (INFO/DP4) [2]
	c, SnpCluster  INT1,INT2    		Filters clusters of 'INT1' or more SNPs within a run of 'INT2' bases []
	d, MinDP  INT               		Minimum read depth (INFO/DP or INFO/DP4) [2]
	D, MaxDP  INT               		Maximum read depth (INFO/DP or INFO/DP4) [10000000]
	H, HWE  FLOAT               		Minimum P-value for HWE and F<0 (invokes --fill-HWE) []
	H2, HWE2  FLOAT              		Minimum P-value for HWE (plus F<0) (INFO/AC and INFO/AN or --fill-AC-AN) []
	HG, HWE_G3  FLOAT            		Minimum P-value for HWE and F<0 (INFO/HWE and INFO/G3) []
	Q, Qual  INT                		Minimum value of the QUAL field [10]
	q, MinMQ  INT               		Minimum RMS mapping quality for SNPs (INFO/MQ) [10]
	r, RefN                     		Reference base is N []
	v, VDB  FLOAT               		Minimum Variant Distance Bias (INFO/VDB) [0]
	w, SnpGap  INT              		SNP within INT bp around a gap to be filtered [10]
	W, GapWin  INT              		Window size for filtering adjacent gaps [3]
Examples:
   zcat in.vcf.gz | vcf-annotate -a annotations.gz -d descriptions.txt -c FROM,TO,CHROM,ID,INFO/DP | bgzip -c >out.vcf.gz 
   zcat in.vcf.gz | vcf-annotate -f +/-a/c=3,10/q=3/d=5/-D -a annotations.gz -d key=INFO,ID=GN,Number=1,Type=String,Description='Gene Name' | bgzip -c >out.vcf.gz 
   zcat in.vcf.gz | vcf-annotate -a dbSNPv132.tab.gz -c CHROM,POS,REF,ALT,ID,-,-,- | bgzip -c >out.vcf.gz 
   zcat in.vcf.gz | vcf-annotate -r FILTER/MinDP | bgzip -c >out.vcf.gz 
Where descriptions.txt contains:
   key=INFO,ID=GN,Number=1,Type=String,Description='Gene Name'
   key=INFO,ID=STR,Number=1,Type=Integer,Description='Strand'
The file dbSNPv132.tab.gz with dbSNP IDs can be downloaded from
   ftp://ftp.sanger.ac.uk/pub/1000genomes/pd3/dbSNP/
```

## Captured Man Page

```text
No man page captured.
```

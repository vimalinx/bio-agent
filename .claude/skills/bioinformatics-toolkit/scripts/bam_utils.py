#!/usr/bin/env python3
"""
BAM file utility functions for bioinformatics workflows.
Requires pysam: pip install pysam
"""

import sys
import subprocess


def bam_stats(bam_file):
    """Get comprehensive BAM file statistics."""
    # Run samtools flagstat
    result = subprocess.run(
        ["samtools", "flagstat", bam_file],
        capture_output=True,
        text=True
    )
    return result.stdout


def count_mapped_reads(bam_file):
    """Count mapped reads in BAM file."""
    result = subprocess.run(
        ["samtools", "view", "-c", "-F", "4", bam_file],
        capture_output=True,
        text=True
    )
    return int(result.stdout.strip())


def count_unmapped_reads(bam_file):
    """Count unmapped reads in BAM file."""
    result = subprocess.run(
        ["samtools", "view", "-c", "-f", "4", bam_file],
        capture_output=True,
        text=True
    )
    return int(result.stdout.strip())


def get_coverage(bam_file):
    """Get coverage statistics from BAM file."""
    result = subprocess.run(
        ["samtools", "depth", bam_file],
        capture_output=True,
        text=True
    )

    if not result.stdout:
        return {"mean": 0, "max": 0, "min": 0}

    depths = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) >= 3:
                depths.append(int(parts[2]))

    if not depths:
        return {"mean": 0, "max": 0, "min": 0}

    return {
        "mean": sum(depths) / len(depths),
        "max": max(depths),
        "min": min(depths)
    }


def extract_chromosome(bam_file, output_bam, chromosome):
    """Extract reads for a specific chromosome."""
    result = subprocess.run(
        ["samtools", "view", "-b", bam_file, chromosome],
        capture_output=True
    )

    with open(output_bam, 'wb') as f:
        f.write(result.stdout)

    # Index the extracted BAM
    subprocess.run(["samtools", "index", output_bam])
    return output_bam


def filter_by_mapping_quality(bam_file, output_bam, min_quality=20):
    """Filter BAM by mapping quality."""
    subprocess.run([
        "samtools", "view", "-b",
        "-q", str(min_quality),
        bam_file
    ], stdout=open(output_bam, 'w'))

    # Index the filtered BAM
    subprocess.run(["samtools", "index", output_bam])
    return output_bam


def bam_to_fastq(bam_file, output_fastq):
    """Convert BAM to FASTQ."""
    subprocess.run([
        "samtools", "fastq",
        bam_file,
        "-0", output_fastq
    ])
    return output_fastq


def merge_bam_files(input_bams, output_bam):
    """Merge multiple BAM files."""
    cmd = ["samtools", "merge", output_bam] + input_bams
    subprocess.run(cmd)

    # Index merged BAM
    subprocess.run(["samtools", "index", output_bam])
    return output_bam


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: python bam_utils.py <command> [options]")
        print("Commands:")
        print("  stats <bam>                      - Get BAM statistics")
        print("  count-mapped <bam>               - Count mapped reads")
        print("  count-unmapped <bam>             - Count unmapped reads")
        print("  coverage <bam>                   - Get coverage stats")
        print("  extract-chr <bam> <chr> <output> - Extract chromosome")
        print("  filter-qual <bam> <output> <min> - Filter by quality")
        print("  to-fastq <bam> <fastq>          - Convert to FASTQ")
        print("  merge <output> <bam1> <bam2> ... - Merge BAM files")
        sys.exit(1)

    command = sys.argv[1]

    if command == "stats":
        if len(sys.argv) < 3:
            print("Usage: bam_utils.py stats <bam>")
            sys.exit(1)
        stats = bam_stats(sys.argv[2])
        print(stats)

    elif command == "count-mapped":
        if len(sys.argv) < 3:
            print("Usage: bam_utils.py count-mapped <bam>")
            sys.exit(1)
        count = count_mapped_reads(sys.argv[2])
        print(f"Mapped reads: {count}")

    elif command == "count-unmapped":
        if len(sys.argv) < 3:
            print("Usage: bam_utils.py count-unmapped <bam>")
            sys.exit(1)
        count = count_unmapped_reads(sys.argv[2])
        print(f"Unmapped reads: {count}")

    elif command == "coverage":
        if len(sys.argv) < 3:
            print("Usage: bam_utils.py coverage <bam>")
            sys.exit(1)
        cov = get_coverage(sys.argv[2])
        print(f"Mean coverage: {cov['mean']:.2f}")
        print(f"Max coverage: {cov['max']}")
        print(f"Min coverage: {cov['min']}")

    elif command == "extract-chr":
        if len(sys.argv) < 5:
            print("Usage: bam_utils.py extract-chr <bam> <chr> <output>")
            sys.exit(1)
        extract_chromosome(sys.argv[2], sys.argv[4], sys.argv[3])
        print(f"Extracted {sys.argv[3]} to {sys.argv[4]}")

    elif command == "filter-qual":
        if len(sys.argv) < 4:
            print("Usage: bam_utils.py filter-qual <bam> <output> [min_quality]")
            sys.exit(1)
        min_qual = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        filter_by_mapping_quality(sys.argv[2], sys.argv[3], min_qual)
        print(f"Filtered {sys.argv[2]} to {sys.argv[3]} (quality >= {min_qual})")

    elif command == "to-fastq":
        if len(sys.argv) < 4:
            print("Usage: bam_utils.py to-fastq <bam> <fastq>")
            sys.exit(1)
        bam_to_fastq(sys.argv[2], sys.argv[3])
        print(f"Converted {sys.argv[2]} to {sys.argv[3]}")

    elif command == "merge":
        if len(sys.argv) < 4:
            print("Usage: bam_utils.py merge <output> <bam1> <bam2> ...")
            sys.exit(1)
        output_bam = sys.argv[2]
        input_bams = sys.argv[3:]
        merge_bam_files(input_bams, output_bam)
        print(f"Merged {len(input_bams)} BAM files to {output_bam}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

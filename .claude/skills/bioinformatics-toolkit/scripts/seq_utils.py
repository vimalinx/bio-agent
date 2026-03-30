#!/usr/bin/env python3
"""
Sequence utility functions for bioinformatics workflows.
Can be called directly or imported as a module.
"""

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def count_sequences(fasta_file):
    """Count sequences in a FASTA file."""
    count = sum(1 for _ in SeqIO.parse(fasta_file, "fasta"))
    return count


def get_sequence_lengths(fasta_file):
    """Get lengths of all sequences in a FASTA file."""
    lengths = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        lengths.append((record.id, len(record.seq)))
    return lengths


def reverse_complement(input_file, output_file):
    """Create reverse complement of sequences."""
    records = []
    for record in SeqIO.parse(input_file, "fasta"):
        rc_seq = record.seq.reverse_complement()
        rc_record = SeqRecord(
            rc_seq,
            id=f"{record.id}_RC",
            description=f"Reverse complement of {record.id}"
        )
        records.append(rc_record)

    SeqIO.write(records, output_file, "fasta")
    return len(records)


def extract_sequences(input_file, output_file, seq_ids):
    """Extract specific sequences by ID."""
    seq_ids_set = set(seq_ids)
    records = [
        record for record in SeqIO.parse(input_file, "fasta")
        if record.id in seq_ids_set
    ]
    SeqIO.write(records, output_file, "fasta")
    return len(records)


def translate_nucleotide(input_file, output_file):
    """Translate nucleotide sequences to amino acids."""
    records = []
    for record in SeqIO.parse(input_file, "fasta"):
        protein = record.seq.translate(to_stop=True)
        protein_record = SeqRecord(
            protein,
            id=record.id,
            description=f"Translation of {record.id}"
        )
        records.append(protein_record)

    SeqIO.write(records, output_file, "fasta")
    return len(records)


def filter_by_length(input_file, output_file, min_length=0, max_length=float('inf')):
    """Filter sequences by length."""
    records = [
        record for record in SeqIO.parse(input_file, "fasta")
        if min_length <= len(record.seq) <= max_length
    ]
    SeqIO.write(records, output_file, "fasta")
    return len(records)


def gc_content(sequence):
    """Calculate GC content of a sequence."""
    gc = sequence.upper().count('G') + sequence.upper().count('C')
    return 100 * gc / len(sequence) if len(sequence) > 0 else 0


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: python seq_utils.py <command> [options]")
        print("Commands:")
        print("  count <fasta>                    - Count sequences")
        print("  lengths <fasta>                  - Get sequence lengths")
        print("  revcomp <input> <output>         - Reverse complement")
        print("  translate <input> <output>       - Translate to protein")
        print("  gc <fasta>                       - Calculate GC content")
        sys.exit(1)

    command = sys.argv[1]

    if command == "count":
        if len(sys.argv) < 3:
            print("Usage: seq_utils.py count <fasta>")
            sys.exit(1)
        count = count_sequences(sys.argv[2])
        print(f"Total sequences: {count}")

    elif command == "lengths":
        if len(sys.argv) < 3:
            print("Usage: seq_utils.py lengths <fasta>")
            sys.exit(1)
        lengths = get_sequence_lengths(sys.argv[2])
        for seq_id, length in lengths:
            print(f"{seq_id}\t{length}")

    elif command == "revcomp":
        if len(sys.argv) < 4:
            print("Usage: seq_utils.py revcomp <input> <output>")
            sys.exit(1)
        count = reverse_complement(sys.argv[2], sys.argv[3])
        print(f"Created {count} reverse complement sequences")

    elif command == "translate":
        if len(sys.argv) < 4:
            print("Usage: seq_utils.py translate <input> <output>")
            sys.exit(1)
        count = translate_nucleotide(sys.argv[2], sys.argv[3])
        print(f"Translated {count} sequences")

    elif command == "gc":
        if len(sys.argv) < 3:
            print("Usage: seq_utils.py gc <fasta>")
            sys.exit(1)
        for record in SeqIO.parse(sys.argv[2], "fasta"):
            gc = gc_content(record.seq)
            print(f"{record.id}\t{gc:.2f}%")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

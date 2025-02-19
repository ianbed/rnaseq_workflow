"""Snakemake wrapper for trimming paired-end reads using trim_galore."""

__author__ = "Kerrin Mendler"
__copyright__ = "Copyright 2018, Kerrin Mendler"
__email__ = "mendlerke@gmail.com"
__license__ = "MIT"


from snakemake.shell import shell
import os.path


log = snakemake.log_fmt_shell()

# Check that two input files were supplied
n_reads = len([snakemake.input.reads])
n_fastqc_html = len(snakemake.input.fastqc_html)
n_fastqc_zip = len(snakemake.input.fastqc_zip)

assert n_reads == 1, "Input must contain 1 fastq files. Given: %r." % [n_reads,snakemake.input.reads]
assert n_fastqc_html == 1, "Input must contain 1 fastqc html reports. Given: %r." % n_fastqc_html
assert n_fastqc_zip == 1, "Input must contain 1 fastqc .zip files. Given: %r." % n_fastqc_zip

# Don't run with `--fastqc` flag
if "--fastqc" in snakemake.params.get("extra", ""):
    raise ValueError("The trim_galore Snakemake wrapper cannot "
                       "be run with the `--fastqc` flag. Please "
                       "remove the flag from extra params. "
                       "You can use the fastqc Snakemake wrapper on "
                       "the input and output files instead.")

# Check that four output files were supplied
m = len(snakemake.output)
assert m == 2, "Output must contain 2 files. Given: %r." % m

# Check that all output files are in the same directory
out_dir = os.path.dirname(snakemake.output[0])
for file_path in snakemake.output[1:]:
    assert out_dir == os.path.dirname(file_path), \
        "trim_galore can only output files to a single directory." \
        " Please indicate only one directory for the output files."

shell(
    "(trim_galore"
    " {snakemake.params.extra}"
    " -o {out_dir}"
    " {snakemake.input.reads})"
    " {log}")

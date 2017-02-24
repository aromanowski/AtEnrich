# AtEnrich

AtEnrich is a simple command-line tool for calculating enrichment of gene lists or clusters of genes across a variety of curated gene lists from functional genomic experiments.

### Prerequisites

This software requires the numpy, scipy, and pandas packages. These will be installed automatically through pip installation if not already installed.

### Installing

The simplest way to install atenrich is from PyPI using pip:

```
pip install atenrich
```

## Running AtEnrich

AtEnrich can be run from the command line either for enrichment of a single gene list against a background gene list, or enrichment across a set of clusters. In list mode:

```
example
```

Here, 'list_filename' is a plaintext file of the form:

```
background_locus_id_0 list_of_interest_locus_id_0
background_locus_id_1 list_of_interest_locus_id_1
background_locus_id_2 list_of_interest_locus_id_2
background_locus_id_3 list_of_interest_locus_id_3
...                   ...
```
Locus identifiers are given by the Arabidopsis Genome Initiative (AGI) names (e.g. 'AT1G09570' for PHYA). Tabs separate the background gene list (left-hand column) and the list of interest (right-hand column). The genes of interest must be a subset of the background gene list.

In cluster mode:

```
atenrich --mode cluster example_data/seaton2017_all_clusters_atenrich_input.csv example_data/cluster_mode_output
```

Here, 'cluster_filename' is a plaintext file of the form:

```
locus_id_0  cluster_label_for_locus_id_0
locus_id_1  cluster_label_for_locus_id_1
locus_id_2  cluster_label_for_locus_id_2
locus_id_3  cluster_label_for_locus_id_3
...         ...
```

## Authors

* **Daniel Seaton** (https://github.com/danielseaton)

## License



## Acknowledgments


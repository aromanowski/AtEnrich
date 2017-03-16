# AtEnrich

AtEnrich is a simple command-line tool for calculating enrichment of gene lists or clusters of genes across a variety of curated gene lists from functional genomic experiments.

### Prerequisites

This software runs on Unix operating systems (tested on Linux (Ubuntu) and Mac OS). It requires python 2.7 with the numpy, scipy, and pandas packages. These will be installed automatically through pip installation if not already installed.

### Installing

The simplest way to install AtEnrich is from PyPI using pip:

```
pip install atenrich
```

Alternatively, install by running (from the top directory):

```
python setup.py install
```

## Running AtEnrich

AtEnrich can be run from the command line either for enrichment of a single gene list against a background gene list, or enrichment across a set of clusters. In list mode:

```
atenrich --mode list input_filename output_prefix
```
Here, the 'output_string' denotes the prefix used for files - the output files are then 'output_string_pvals.txt' and 'output_string_FE.txt'. 'list_filename' is a tab-delimited plaintext file of the form:

```
background_locus_id_0 list_of_interest_locus_id_0
background_locus_id_1 list_of_interest_locus_id_1
background_locus_id_2 list_of_interest_locus_id_2
background_locus_id_3 list_of_interest_locus_id_3
...                   ...
```
Locus identifiers are given by the Arabidopsis Genome Initiative (AGI) names (e.g. 'AT1G09570' for PHYA). Tabs separate the background gene list (left-hand column) and the list of interest (right-hand column). The genes of interest must be a subset of the background gene list.


In cluster mode, enrichment across all clusters can be evaluated:

```
atenrich --mode cluster input_filename output_prefix
```

Here, 'cluster_filename' is a tab-delimited plaintext file of the form:

```
locus_id_0  cluster_label_for_locus_id_0
locus_id_1  cluster_label_for_locus_id_1
locus_id_2  cluster_label_for_locus_id_2
locus_id_3  cluster_label_for_locus_id_3
...         ...
```

## Worked example

For the clustering of genes analysed in Seaton et al, 2017:

```
atenrich --mode cluster example_data/seaton2017_all_clusters_atenrich_input.csv example_data/cluster_mode_output
```

For just cluster 85 of this clustering:

```
atenrich --mode list example_data/seaton2017_cluster_85_atenrich_input.csv example_data/list_mode_output
```

## GeneListDB

The gene list database file is an SQLite relational database, stored in the file: atenrich/data/db/GeneListDB.db. The tables in this file can be browsed using a SQLite file browser such as Sqliteman. The database file can be changed to add user-supplied gene lists using scripts from https://github.com/danielseaton/GeneListDB.


## Authors

* **Daniel Seaton** (https://github.com/danielseaton)

## License



## Acknowledgments


#!/usr/bin/env python
import click,calculate_enrichment
import pandas as pd

@click.command()
@click.option("--mode",default='cluster', help="Enrichment mode (list or cluster).")
@click.option("--header",default=False,is_flag=True,help="Flag to be specified if there is a header in the input file.")
@click.argument("input",type=click.Path(exists=True,dir_okay=False,readable=True))
@click.argument("output",nargs=1)

def main(input,output,mode,header):
    """Dummy function that prints arguments to console and copies input to output."""
    click.echo("AtEnrich running in {0} mode.".format(mode))

    db_id = 'GeneListDB'

    if header:
        offset = 1
    else:
        offset = 0
    
    with open(click.format_filename(input)) as data_file:
        lines = [x.strip().split('\t') for x in data_file.readlines()[offset:]]

    #First column is always the background gene list    
    background_gene_list = [x[0] for x in lines]

    if mode=='cluster':
        #Second column is a list of integer cluster labels
        cluster_labels = [int(x[1]) for x in lines]
        pval_df,FE_df = calculate_enrichment.calculate_enrichment(cluster_labels,mode,background_gene_list,db_id,cluster_indices=None)
    elif mode=='list':
        #Second column is a subset of gene ids
        gene_list = [x[1] for x in lines if len(x)==2]
        assert(len(set(background_gene_list)&set(gene_list))==len(set(gene_list)))
        pval_df,FE_df = calculate_enrichment.calculate_enrichment(gene_list,mode,background_gene_list,db_id,cluster_indices=None)
    

    #output to file
    pval_df.to_csv(click.format_filename(output+'_pval.txt'),sep='\t')
    FE_df.to_csv(click.format_filename(output+'_FE.txt'),sep='\t')

if __name__ == '__main__':
    main()
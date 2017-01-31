#!/usr/bin/env python
import click,analyse_clustering
import pandas as pd

@click.command()
@click.option("--mode",default='cluster', help="Enrichment mode (list or cluster).")
@click.option("--header",default=False,is_flag=True,help="Flag to be specified if there is a header in the input file.")
@click.argument("input",type=click.Path(exists=True,dir_okay=False,readable=True))
@click.argument("output",nargs=1)

def main(input,output,mode,header):
    """Dummy function that prints arguments to console and copies input to output."""
    click.echo("AtEnrich running in {0} mode.".format(mode))

    if header:
        header_row = 0
    else:
        header_row = None
    input_df = pd.read_csv(click.format_filename(input),header=header_row,sep='\t')

    cData = dict()
    cData['gene_list'] = input_df.ix[:,0]
    cData['labels'] = input_df.ix[:,1]
    db_id = 'GeneListDB'
    pval_df,FE_df = analyse_clustering.analyse_clustering(cData,db_id,method='pval',feature_list=None,excluded_features=None,cluster_indices=None,feature_combinations=[])
    pval_df.to_csv(click.format_filename(output+'_pval.txt'),sep='\t')
    FE_df.to_csv(click.format_filename(output+'_FE.txt'),sep='\t')

if __name__ == '__main__':
    main()
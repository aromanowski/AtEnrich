#!/usr/bin/env python
import click,clusterdata,analyse_clustering

@click.command()
@click.option("--mode",default='cluster', help="Enrichment mode (list or cluster).")
#@click.option("--backgound",default=None,help="Name of background gene list file if running in list mode.")
@click.argument("input")
@click.argument("output")

def main(input,output,mode):
    """Dummy function that prints arguments to console and copies input to output."""
    click.echo("AtEnrich running in {0} mode.".format(mode))
    cData = clusterdata.ClusterData.from_txt(input)
    db_id = 'GeneListDB'
    pval_df = analyse_clustering.analyse_clustering(cData,db_id,method='pval',feature_list=None,excluded_features=None,cluster_indices=None,feature_combinations=[])
    pval_df.to_csv(output,sep='\t')

if __name__ == '__main__':
    main()
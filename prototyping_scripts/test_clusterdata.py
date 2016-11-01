import GAFER
import os
import inspect

#main_dir = os.path.dirname(inspect.getfile())
main_dir = os.getcwd()
data_dir = os.path.join(main_dir,'test_data_files')

clustering_file_location = os.path.join(data_dir,'diurnal_clustering_300916.json')

clusters = GAFER.ClusterData.from_json(clustering_file_location)

clusters.get_cluster_label('AT3G51240')
clusters.get_cluster_label('AT1G09570')
""">>> clusters.get_cluster_label('AT3G51240')
85
>>> clusters.get_cluster_label('AT1G09570')
6
"""
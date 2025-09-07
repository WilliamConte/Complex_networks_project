import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import igraph as ig
from io import StringIO
import glob
import os
from helper_functions import *

def extract_data_pipeline_no_topology(file_pattern_topologies, single_filename_lines, filename_nodes, output_edges, output_nodes,
                          city_path = "./Berlin", file_prefix = "berlin-", file_suffix = ".txt", line_prefixes=None, more_files=False, separator = True):
    #edges

    df_edges, dict_key = edges_from_adjacency(file_pattern_topologies, filename_nodes)
    stations_grouped = get_lines_from_file(single_filename_lines, dict_key, city_path, file_prefix, file_suffix, 
                                           line_prefixes, more_files, separator)
    df_edges = assign_line_ordered(df_edges,stations_grouped)
    df_edges = add_labels(df_edges,dict_key)

    #nodes
    
    df_nodes = get_nodes_from_file(filename_nodes, df_edges)
    df_edges, df_nodes = reset_ID(df_edges,df_nodes)
    save_lists(df_edges, df_nodes, output_edges, output_nodes)

    return 
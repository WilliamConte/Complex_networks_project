#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import igraph as ig
from io import StringIO
import glob
import os
from helper_functions import *
from extract_data_pipeline import *
from extract_data_pipeline_no_topology import *


# In[2]:


file_pattern_topologies = "./Madrid/madrid-topologies-noLR/Madrid-*-adjacency-number.txt"
file_lines = None
line_prefixes = ["line","ramal"]
filename_nodes = "./Madrid/madrid-stations-times.txt"

city_path = "./Madrid"
file_prefix = "madrid-"
file_suffix = ".txt"

output_edges = "Madrid_edgelist.csv"
output_nodes = "Madrid_nodelist.csv"

extract_data_pipeline_no_topology(file_pattern_topologies, file_lines, filename_nodes, output_edges, output_nodes, city_path = city_path, 
                      file_prefix = file_prefix, file_suffix = file_suffix,  line_prefixes=line_prefixes, more_files = True)


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


# In[2]:


file_pattern_topologies = "./HongKong/HongKong-topologies/HongKong-*-matrix.mat"
file_lines = "./HongKong/HK-stations-times.txt"
line_prefixes = ["line"]
filename_nodes = file_lines

city_path = "./HongKong"
file_prefix = "HK-"
file_suffix = ".txt"

output_edges = "HongKong_edgelist.csv"
output_nodes = "HongKong_nodelist.csv"

extract_data_pipeline(file_pattern_topologies, file_lines, filename_nodes, output_edges, output_nodes, city_path = city_path, 
                      file_prefix = file_prefix, file_suffix = file_suffix,  line_prefixes=line_prefixes, more_files = True)


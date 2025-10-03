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


file_pattern_topologies = "./Barcelona/Barcelona-topologies/Barcelona-*-matrix.mat"
file_lines = "./Barcelona/barcelona-stations-positions-years+.txt"
line_prefixes = ["Line"]
filename_nodes = "./Barcelona/barcelona-stations-positions-years.txt"
output_edges = "Barcelona_edgelist.csv"
output_nodes = "Barcelona_nodelist.csv"

extract_data_pipeline(file_pattern_topologies, file_lines, filename_nodes, 
                      output_edges, output_nodes, line_prefixes=line_prefixes)


# In[ ]:





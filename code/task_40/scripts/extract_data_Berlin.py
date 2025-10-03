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


file_pattern_topologies = "./Berlin/Berlin-topologies/Berlin-*-matrix.mat"
line_prefixes = ["u", "alteu3", "neueu3"]
filename_nodes = "./Berlin/berlin-stations-positions-years.txt"
output_edges = "Berlin_edgelist.csv"
output_nodes = "Berlin_nodelist.csv"

extract_data_pipeline(file_pattern_topologies, None, filename_nodes, 
                      output_edges, output_nodes, line_prefixes=line_prefixes, more_files=True)


# In[ ]:





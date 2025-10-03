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


# # Edgelist

# In[2]:


file_pattern = "./Beijing/Beijing-topologies/Beijing-*-matrix.mat"
df_edges, dict_key = edges_from_topology(file_pattern)


# ### Find the line

# In[3]:


filename = "./Beijing/beijing-stations-positions-years2.txt"
line_prefixes = ["Line", "Batong", "Daxing", "Yzhuang", "Changping", "Airport"]  
stations_grouped = get_lines_from_file(filename,dict_key, line_prefixes)


# In[4]:


df_edges = assign_line(df_edges,stations_grouped)


# In[5]:


df_edges = add_labels(df_edges,dict_key)


# # Nodelist

# In[6]:


filename = "./Beijing/beijing-stations-positions-years.txt"

df_nodes = get_nodes_from_file(filename, df_edges)


# ### Remap indices

# In[7]:


df_edges, df_nodes = reset_ID(df_edges,df_nodes)


# In[8]:


save_lists(df_edges, df_nodes, "Beijing_edgelist.csv", "Beijing_nodelist.csv")


# In[9]:


file_pattern_topologies = "./Beijing/Beijing-topologies/Beijing-*-matrix.mat"
file_lines = "./Beijing/beijing-stations-positions-years2.txt"
line_prefixes = ["Line", "Batong", "Daxing", "Yzhuang", "Changping", "Airport"]
filename_nodes = "./Beijing/beijing-stations-positions-years.txt"
output_edges = "Beijing_edgelist.csv"
output_nodes = "Beijing_nodelist.csv"

extract_data_pipeline(file_pattern_topologies, file_lines, filename_nodes, 
                      output_edges, output_nodes, line_prefixes=line_prefixes)


# In[ ]:





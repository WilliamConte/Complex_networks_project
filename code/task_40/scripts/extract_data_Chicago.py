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
import re
from helper_functions import *
from extract_data_pipeline import *
from extract_data_pipeline_no_topology import *
from extract_data_pipeline_from_lines import *


# In[2]:


file_values = np.arange(1,9)  # Or any list of suffixes you want
file_pattern_template = "./Chicago/chicago-line{}.txt"
file_pattern_topologies = [file_pattern_template.format(v) for v in file_values]



file_lines = None
line_prefixes = ["line1","line2","line3","line4","line5","line6","line7","line8"]
file_nodes = "./Chicago/chicago-stations-positions-years.txt"

city_path = "./Chicago"
file_prefix = "chicago-"
file_suffix = ".txt"

output_edges = "Chicago_edgelist.csv"
output_nodes = "Chicago_nodelist.csv"


# In[3]:


extract_data_pipeline_from_lines(file_pattern_topologies, file_lines, file_nodes, output_edges, output_nodes, city_path = city_path, 
                      file_prefix = file_prefix, file_suffix = file_suffix,  line_prefixes=line_prefixes, more_files = True)


# In[ ]:





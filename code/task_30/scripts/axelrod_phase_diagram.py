#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import igraph as ig
from collections import Counter, deque, defaultdict
import multiprocessing as mp
import matplotlib.pyplot as plt
from functools import partial
from helpers_dynamics_axelrod import *
from helpers_phase_diagram import *


# In[2]:


F_values = np.arange(2,6,1)
q_values = np.linspace(2,200,20,dtype=int)
runs = 1
N = 1000


# ## ER

# In[3]:


results = create_phase_diagram(F_values, q_values, N = N, type = 'ER', p = 0.01, runs = 1)


# In[4]:


plot_phase_diagram(F_values,q_values,results,"Phase diagram - Erdos Renyi (p=0.01)", plotname="phase_diagram_ER.pdf")


# ## BA

# In[6]:


results = create_phase_diagram(F_values, q_values, N = N, type = 'BA', m = 5, p = None)


# In[7]:


plot_phase_diagram(F_values,q_values,results,"Phase diagram - Barabasi Albert (m=5)",  plotname="phase_diagram_BA.pdf")


# ## WS

# In[8]:


results = create_phase_diagram(F_values, q_values, N = N, type = 'WS', m = None, p = None, nei=5, p_ws=0.03)


# In[9]:


plot_phase_diagram(F_values,q_values,results,"Phase diagram - Watts Strogratz (nei=5, p=0.03)", plotname="phase_diagram_WS.pdf")


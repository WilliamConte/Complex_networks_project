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


# In[2]:


# Parameters
steps = 20_000_000
runs = 10
q_values = [2,10,40,80,120,200]  # number of traits
F = 5   # number of features
N = 1000
save_interval = 10000


# ## ER

# In[3]:


Smax_per_q,active_bonds_per_q,std_Smax_per_q,std_active_bonds_per_q = run_simulations(F, q_values, N, type='ER', p=0.01, m=None, nei=None, p_ws=None, save_csv=True, filename="dynamics_ER_001.csv")


# In[4]:


plot_evolution(Smax_per_q,active_bonds_per_q,std_Smax_per_q,std_active_bonds_per_q,q_values,'Evolution of Active Bonds ER (p=0.01)', 'Evolution of Smax ER (p=0.01)',
               plotname='evolution_plot_ER.pdf')


# ## BA

# In[5]:


Smax_per_q,active_bonds_per_q,std_Smax_per_q,std_active_bonds_per_q = run_simulations(F, q_values, N, type='BA', p=None, m=5, nei=None, p_ws=None, save_csv=True, filename="dynamics_BA_m5.csv",)


# In[8]:


plot_evolution(Smax_per_q,active_bonds_per_q,std_Smax_per_q,std_active_bonds_per_q,q_values,'Evolution of Active Bonds BA (m=5)', 'Evolution of Smax BA (m=5)',
               plotname='evolution_plot_BA.pdf')


# ## WS

# In[11]:


Smax_per_q,active_bonds_per_q,std_Smax_per_q,std_active_bonds_per_q = run_simulations(F, q_values, N, type='WS', p=None, m=None, nei=5, p_ws=0.03, save_csv=True, filename="dynamics_WS_nei5_p003.csv")


# In[12]:


plot_evolution(Smax_per_q,active_bonds_per_q,std_Smax_per_q,std_active_bonds_per_q,q_values,'Evolution of Active Bonds WS (nei=5, p=0.03)', 'Evolution of Smax BA WS (nei=5, p=0.03)',
               plotname='evolution_plot_WS.pdf')


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
from helpers_phase_transitions import *


# In[2]:


# --- Parameters
steps = 20_000_000
runs = 10
q_values = [2, 10, 20, 40, 60, 80, 100, 120, 140, 150, 160, 180, 200]
F = 5     # number of features
N = 1000
save_interval = 10000


# ## ER

# In[3]:


Smax_per_q, std_Smax_per_q = run_phase_transition_simulation(F, q_values, N, type='ER', p=0.01, m=None, nei=None, p_ws=None)


# In[4]:


plot_phase_transition(q_values, Smax_per_q, std_Smax_per_q, "Axelrod Model phase transition - ER (p=0.01)", plotname='phase_transition_ER.pdf')


# ## BA

# In[5]:


Smax_per_q, std_Smax_per_q = run_phase_transition_simulation(F, q_values, N, type='BA', p=None, m=5, nei=None, p_ws=None)


# In[6]:


plot_phase_transition(q_values, Smax_per_q, std_Smax_per_q, "Axelrod Model phase transition - BA (m=5)", plotname='phase_transition_BA.pdf')


# ## WS

# In[7]:


Smax_per_q, std_Smax_per_q = run_phase_transition_simulation(F, q_values, N, type='WS', p=None, m=None, nei=5, p_ws=0.03)


# In[8]:


plot_phase_transition(q_values, Smax_per_q, std_Smax_per_q, "Axelrod Model phase transition - WS (nei=5, p=0.03)", plotname='phase_transition_WS.pdf')


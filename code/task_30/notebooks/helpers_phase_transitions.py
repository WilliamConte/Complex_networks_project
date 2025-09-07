import numpy as np
import igraph as ig
from collections import Counter, deque, defaultdict
import multiprocessing as mp
import matplotlib.pyplot as plt
from functools import partial
from helpers_dynamics_axelrod import *

def run_phase_transition_simulation(F, q_values, N=1000, is_real = False, real_g = None, type='ER', p=0.01, m=None, nei=None, p_ws=None, runs = 10):
    Smax_per_q = np.zeros(len(q_values))  
    std_Smax_per_q = np.zeros(len(q_values))  

    for i, q in enumerate(q_values):
        print('q =', q)
        result = run_q_simulation(F=F, q=q, N=N, is_real=is_real, real_g=real_g, 
                                      type = type, p=p, m=m, nei=nei, 
                                      p_ws=p_ws)
        S_max_all, _ = zip(*result)
        S_max_all = np.array(S_max_all)
    
        #final values only
        mean_Smax = np.mean(S_max_all, axis=0)[-1]  
        std_Smax = np.std(S_max_all, axis=0)[-1]    
    
        # Store scalar values in 1D arrays
        Smax_per_q[i] = mean_Smax
        std_Smax_per_q[i] = std_Smax/np.sqrt(runs)
    
    return Smax_per_q, std_Smax_per_q


def plot_phase_transition(q_values , Smax_per_q, std_Smax_per_q, title, plotname):
    plt.figure(figsize=(8,5))

    plt.errorbar(q_values, Smax_per_q, yerr=std_Smax_per_q, fmt='-o', capsize=5, markersize=8,
                markerfacecolor='skyblue', markeredgecolor='navy', ecolor='red', elinewidth=2, capthick=2)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel("q", fontsize=14)
    plt.ylabel("Smax/N", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylim(0, 1.05)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(plotname)
    plt.show()

    return 
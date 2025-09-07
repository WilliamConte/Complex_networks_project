import numpy as np
import igraph as ig
from collections import Counter, deque, defaultdict
import multiprocessing as mp
import matplotlib.pyplot as plt
from functools import partial
from helpers_dynamics_axelrod import *

def create_phase_diagram(F_values, q_values, is_real = False, real_g = None, N=1000, type='ER', p=0.01, m=None, 
                         nei=None, p_ws=None, runs = 10):
    results = []  # will hold tuples (F, q, avg_final_Smax)
    
    for F in F_values:
        for q in q_values:
            print("F =",F,"q =", q)
            # Run multiple simulations for this (F,q)
            result = run_q_simulation(F=F, q=q, N=N, is_real=is_real, real_g=real_g, 
                                      type = type, p=p, m=m, nei=nei, p_ws=p_ws, runs = runs)
            
            # Extract the final S_max for each run
            final_Smax_vals = [sim[0][-1] for sim in result]  # last value in S_max_run for each run
            
            # Average final S_max over all runs
            avg_final_Smax = np.mean(final_Smax_vals)
            results.append((F, q, avg_final_Smax))
    
    return results


def plot_phase_diagram(F_values,q_values,results,title, plotname = ""):
    F_values = sorted(set([x[0] for x in results]))
    q_values = sorted(set([x[1] for x in results]))

    # Create a 2D array to hold values
    heatmap = np.zeros((len(F_values), len(q_values)))

    # Fill the heatmap array
    for F, q, val in results:
        i = F_values.index(F)
        j = q_values.index(q)
        heatmap[i, j] = val

    # Plot heatmap
    plt.figure(figsize=(12,4))
    im = plt.imshow(heatmap, origin='lower', aspect='auto', cmap='viridis')

    # Axis ticks and labels
    plt.xticks(ticks=range(len(q_values)), labels=q_values, fontsize=12)
    plt.yticks(ticks=range(len(F_values)), labels=F_values, fontsize=16)
    plt.xlabel('q', fontsize=16)
    plt.ylabel('F',fontsize=16)
    plt.title(title, fontsize=16)

    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Smax/N', fontsize=14)
    #cbar.set_ticklabels(fontsize = 14)
    plt.tight_layout()
    plt.savefig(plotname)
    plt.show()

    return

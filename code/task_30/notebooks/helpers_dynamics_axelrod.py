import numpy as np
import igraph as ig
from collections import Counter, deque, defaultdict
import multiprocessing as mp
import matplotlib.pyplot as plt
from functools import partial
import pandas as pd

def generate_network(seed, N=2000, is_real = False, real_g = None, type='ER', p=0.01, m=None, nei=None, p_ws=None):
    np.random.seed(seed)
    
    if not is_real:
        if type == 'ER':
            g = ig.Graph.Erdos_Renyi(N, p=p, directed=False, loops=False)

        elif type == 'BA':
            g = ig.Graph.Barabasi(n=N, m=m, directed=False)

        elif type == 'WS':
            g = ig.Graph.Watts_Strogatz(dim=1, size=N, nei=nei, p=p_ws)
    else:
        
        g = real_g

    neighbors_list = g.get_adjlist()
    return g, neighbors_list


def compute_Smax(g, culture_matrix):
    N = g.vcount()
    
    # Convert each culture vector to a tuple for easy hashing
    cultures = [tuple(row) for row in culture_matrix]
    
    # Group nodes by culture
    culture_groups = defaultdict(list)
    for idx, c in enumerate(cultures):
        culture_groups[c].append(idx)
    
    max_cluster_size = 0
    
    for nodes in culture_groups.values():
        if len(nodes) <= max_cluster_size:
            continue  # skip if this group cannot beat current max
        
        visited = set()
        
        for start in nodes:
            if start in visited:
                continue
            
            # BFS starting from 'start'
            queue = deque([start])
            cluster_size = 0
            
            while queue:
                node = queue.popleft()
                if node in visited:
                    continue
                visited.add(node)
                cluster_size += 1
                
                # Only consider neighbors in the same culture group
                for neighbor in g.neighbors(node):
                    if neighbor not in visited and neighbor in nodes:
                        queue.append(neighbor)
            
            max_cluster_size = max(max_cluster_size, cluster_size)
    
    Smax = max_cluster_size / N
    return Smax

def axelrod_run(seed, F, q, is_real = False, real_g = None, N=1000, type='ER', p=0.01, m=None, nei=None, p_ws=None,
                steps=20_000_000, save_interval=10_000):
    np.random.seed(seed)
    
    # Generate network
    g, neighbors_list = generate_network(seed = seed, N = N, is_real = is_real, real_g = real_g, 
                                         type = type, p = p, m = m, nei = nei, p_ws = p_ws)
    E = g.ecount()

    # Initial cultures
    culture_matrix = np.random.randint(low=0, high=q, size=(N, F), dtype=np.int16)
    
    S_max_current = compute_Smax(g, culture_matrix)
    active_bonds = set()
    for node in range(N):
        node_culture = culture_matrix[node]
        for neighbor in neighbors_list[node]:
            if neighbor > node:
                neighbor_culture = culture_matrix[neighbor]
                equal_count = int((node_culture == neighbor_culture).sum())
                if 0 < equal_count < F:
                    active_bonds.add((node, neighbor))
    active_bonds_current = len(active_bonds) / E
    
    # Preallocate
    save_points = steps // save_interval + 1
    S_max_run = np.empty(save_points, dtype=np.float32)
    active_bonds_run = np.empty(save_points, dtype=np.float32)
    
    save_idx = 0
    S_max_run[save_idx] = S_max_current
    active_bonds_run[save_idx] = active_bonds_current
    
    # Simulation loop
    for step in range(steps):
        selected_node = np.random.randint(N)
        neigh = neighbors_list[selected_node]
        
        if neigh:
            selected_neighbor = neigh[np.random.randint(len(neigh))]
            
            pair = tuple(sorted((selected_node, selected_neighbor)))
            if pair in active_bonds:
                node_culture = culture_matrix[selected_node].copy()
                neighbor_culture = culture_matrix[selected_neighbor]
                
                equal_count = int((node_culture == neighbor_culture).sum())
                
                if np.random.rand() < (equal_count / F):
                    diff_idx = np.nonzero(node_culture != neighbor_culture)[0]
                    copied_feature = diff_idx[np.random.randint(len(diff_idx))]
                    
                    node_culture[copied_feature] = neighbor_culture[copied_feature]
                    culture_matrix[selected_node] = node_culture
                    
                    # Update active bonds only for selected_node and its neighbors
                    for neighbor in neighbors_list[selected_node]:
                        updated_pair = tuple(sorted((selected_node, neighbor)))
                        node_culture = culture_matrix[selected_node]
                        neighbor_culture = culture_matrix[neighbor]
                        equal_count = int((node_culture == neighbor_culture).sum())
                        
                        if 0 < equal_count < F:
                            active_bonds.add(updated_pair)
                        elif updated_pair in active_bonds:
                            active_bonds.remove(updated_pair)
                    active_bonds_current = len(active_bonds) / E
        
        # Save only at intervals
        if (step + 1) % save_interval == 0:
            save_idx += 1
            S_max_run[save_idx] = compute_Smax(g, culture_matrix)
            active_bonds_run[save_idx] = active_bonds_current
    
    return S_max_run, active_bonds_run

def run_q_simulation(F, q, N, is_real = False, real_g = None, type='ER', p=0.01, m=None, nei=None, p_ws=None, runs = 10):
    with mp.Pool(processes=mp.cpu_count()) as pool:
        seeds = np.random.randint(0, 2**32 - 1, size=runs)
        function = partial(axelrod_run, N=N, F=F, is_real=is_real, real_g = real_g, q=q, p=p, type=type,  m=m, nei=nei, p_ws=p_ws)
        results = pool.map(function, seeds)
    
    return results


def run_simulations(F, q_values, N, is_real=False, real_g=None, type='ER', p=0.01, 
                   m=None, nei=None, p_ws=None, runs=10, save_csv=False, filename=None):
    
    Smax_per_q = []
    active_bonds_per_q = []
    std_Smax_per_q = []
    std_active_bonds_per_q = []
    
    # For CSV
    csv_data = []
    
    for i, q in enumerate(q_values):
        result = run_q_simulation(F=F, q=q, N=N, is_real=is_real, real_g=real_g,
                                  type=type, p=p, m=m, nei=nei, p_ws=p_ws, runs=runs)
        S_max_all, active_bonds_all = zip(*result)
        S_max_all = np.array(S_max_all)        # shape (runs, timesteps)
        active_bonds_all = np.array(active_bonds_all)
        
        mean_Smax = np.mean(S_max_all, axis=0)
        mean_active_bonds = np.mean(active_bonds_all, axis=0)
        std_Smax = np.std(S_max_all, axis=0)
        std_active_bonds = np.std(active_bonds_all, axis=0)
        
        # Store each individual run *per timestep* for CSV
        if save_csv:
            for run_num in range(runs):
                for t_idx in range(S_max_all.shape[1]):
                    csv_data.append([
                        run_num + 1,  
                        F,
                        q,
                        t_idx,
                        active_bonds_all[run_num, t_idx],
                        S_max_all[run_num, t_idx]
                    ])
   
        Smax_per_q.append(mean_Smax)
        active_bonds_per_q.append(mean_active_bonds)
        std_Smax_per_q.append(std_Smax / np.sqrt(runs))
        std_active_bonds_per_q.append(std_active_bonds / np.sqrt(runs))
    
    # Convert to numpy arrays
    Smax_per_q = np.array(Smax_per_q)
    active_bonds_per_q = np.array(active_bonds_per_q)
    std_Smax_per_q = np.array(std_Smax_per_q)
    std_active_bonds_per_q = np.array(std_active_bonds_per_q)
    
    # Save CSV
    if save_csv:
        if filename is None:
            network_name = 'Real' if is_real else type
            filename = f'axelrod_{network_name}_F{F}.csv'
        
        df = pd.DataFrame(csv_data, columns=['run_number', 'F', 'q', 'timestep',
                                             'active_bonds', 'Smax'])
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")
    
    return Smax_per_q, active_bonds_per_q, std_Smax_per_q, std_active_bonds_per_q


def plot_evolution(Smax_per_q, active_bonds_per_q, std_Smax_per_q, std_active_bonds_per_q, q_values, title1, title2, step_plot = 50, steps = 20_000_000, save_interval = 10_000, plotname = ""):
    iterations = np.arange(0, steps, save_interval -1)
    iterations = iterations[::int(step_plot)]

    # Create figure 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left plot: Active bonds
    for active_bond, std_ab, q in zip(active_bonds_per_q, std_active_bonds_per_q, q_values):
        y_data = active_bond[::step_plot]
        yerr_data = std_ab[::step_plot]
        
        ax1.plot(iterations, y_data, label=f'q = {q}', linewidth=1.5, marker='o', markersize=3)
        ax1.fill_between(iterations, y_data - yerr_data, y_data + yerr_data, alpha=0.3)

    ax1.set_xlabel('Iteration', fontsize = 14)
    ax1.set_ylabel(r'$n_{A}$/ E', fontsize = 14)
    ax1.set_title(title1, fontsize = 16)
    ax1.legend(title='q value', fontsize = 12)
    ax1.grid(True, alpha=0.5)

    # Smax
    for Smax, std_s, q in zip(Smax_per_q, std_Smax_per_q, q_values):
        y_data = Smax[::step_plot]
        yerr_data = std_s[::step_plot]
        
        ax2.plot(iterations, y_data, label=f'q = {q}', linewidth=1.5, marker='o', markersize=3)
        ax2.fill_between(iterations, y_data - yerr_data, y_data + yerr_data, alpha=0.3)

    ax2.set_xlabel('Iteration', fontsize = 14)
    ax2.set_ylabel('Smax / N', fontsize = 14)
    ax2.set_title(title2, fontsize = 16)
    ax2.legend(title='q value', fontsize = 12)
    ax2.grid(True, alpha=0.5)

    plt.tight_layout()
    plt.savefig(plotname)
    
    plt.show()
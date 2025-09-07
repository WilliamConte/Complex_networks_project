import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import igraph as ig
from io import StringIO
from difflib import get_close_matches
import glob
import os
import re

def clean_duplicates(tuple_data):
    seen = set()
    clean_data = []

    for a, b in tuple_data:
        edge = tuple(sorted((a, b)))
        if edge not in seen:
            seen.add(edge)
            clean_data.append(edge)  
    return clean_data



def add_record(df_edges,new_edge,year):
    
    new_row = pd.DataFrame([{
        "nodeID_from": int(new_edge[0]),
        "nodeID_to": int(new_edge[1]),
        "year": year
    }])
    df_edges = pd.concat([df_edges, new_row], ignore_index=True)

    return df_edges.astype(int)

def normalize_station_name(name):
    # Clean and simplify the name
    raw = "".join(name.strip().split()).lower()

    # Manual corrections for known typos or malformed entries
    corrections = {
        "roosevel": "Roosevelt",
        "jacksonpark": "Jackson",
    }

    if raw in corrections:
        corrected = corrections[raw]
        if corrected is None:
            print("PROBELMS, NOT FIND ANY CORRECTIONS", raw, corrected)  # Signal to skip this line entirely
        return corrected

    return raw.title()

def fuzzy_match(name, valid_names, threshold=70):
    matches = get_close_matches(name, valid_names, n=1, cutoff=threshold / 100.0)
    return matches[0] if matches else None

def edges_from_topology(file_pattern):
    
    df_edges = pd.DataFrame({"nodeID_from" : [], "nodeID_to":[], "year":[]})
    dict_key = {}
    old_edges = []

    files = sorted(glob.glob(file_pattern))

    for filename in files:
        
        print("Processing:", filename)  # Do your processing here
        # Read lines starting from '*Matrix'
        with open(filename, "r") as f:
            lines = f.readlines()

        # Find the line with "*Matrix"
        for i, line in enumerate(lines):
            if line.strip().startswith("*Matrix"):
                dictionary_id = lines[1:i]
                matrix_lines = lines[i+1:]  # skip the "*Matrix" line itself
                break
        else:
            raise ValueError("No '*Matrix' line found in the file.")

        #get adjacency
        matrix_str = ''.join(matrix_lines)
        adj_matrix = np.loadtxt(StringIO(matrix_str))
        #get dictionary
        if not dict_key:
            name_counter = {}  # Track how many times we've seen each name
            for i in range(len(dictionary_id)):
                current_value = dictionary_id[i].split()
                station_name = current_value[1].replace("\\", "").replace('"', "")
                station_id = int(current_value[0]) - 1
                
                # Create unique key for duplicates
                if station_name in name_counter:
                    name_counter[station_name] += 1
                    unique_key = f"{station_name}_{name_counter[station_name]}"
                else:
                    name_counter[station_name] = 1
                    unique_key = station_name
                
                dict_key[unique_key] = station_id

        #get the year:
        basename = os.path.basename(filename)
        year = basename.split("-")[1]
        
        new_links = np.where(adj_matrix==1)
        tuple_data = [ (new_links[0][i],new_links[1][i]) for i in range(len(new_links[0])) ]

        new_edges = clean_duplicates(tuple_data)
        
        if df_edges.empty:
            for new_edge in new_edges:
                df_edges = add_record(df_edges,new_edge,year)
            old_edges = new_edges
        else:
            #check for already existent edges
            new_edges = [i for i in new_edges if i not in old_edges]
            for new_edge in new_edges:
                df_edges = add_record(df_edges,new_edge,year)
            if len(new_edges) != 0:
                old_edges.extend(new_edges)
  
        
    return df_edges,dict_key


def edges_from_adjacency(file_pattern, file_nodes):
    
    df_edges = pd.DataFrame({"nodeID_from" : [], "nodeID_to":[], "year":[]})
    old_edges = []

    files = sorted(glob.glob(file_pattern))

    for filename in files:
        
        print("Processing:", filename)  # Do your processing here
        # Read lines starting from '*Matrix'
        basename = os.path.basename(filename)
        year = basename.split("-")[1]

        with open(filename, "r") as f:
            lines = f.readlines()
            tuple_data = []
            for line in lines:
                edge = line.strip().split()
                tuple_data.append(tuple(edge))
            
            new_edges = clean_duplicates(tuple_data)
            
            if df_edges.empty:
                for new_edge in new_edges:
                    df_edges = add_record(df_edges,new_edge,year)
                old_edges = new_edges
            else:
                #check for already existent edges
                new_edges = [i for i in new_edges if i not in old_edges]
                
                for new_edge in new_edges:
                    df_edges = add_record(df_edges,new_edge,year)
                    
                if len(new_edges) != 0:
                    old_edges.extend(new_edges)
                   
    
    stations = []

    with open(file_nodes, "r", encoding="latin-1") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 0:
                continue  # skip empty lines
            station_name = parts[0].strip()
            if station_name not in stations:
                stations.append(station_name)

    # Now create the dict with sequential IDs
    dict_key = {name: i + 1 for i, name in enumerate(stations)}

    return df_edges,dict_key


def edges_from_lines(file_pattern, file_nodes):
    stations = []

    with open(file_nodes, "r", encoding="latin-1") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            station_name = normalize_station_name(parts[0])
            if station_name not in stations:
                stations.append(station_name)

    # Now create the dict with sequential IDs
    dict_key = {name: i + 1 for i, name in enumerate(stations)}

    if isinstance(file_pattern, str):
        files = sorted(glob.glob(file_pattern))
    else:
        files = sorted(file_pattern)

    df_edges = pd.DataFrame({"nodeID_from": [], "nodeID_to": [], "year": []})
    old_edges = []

    for filename in files:
        print("Processing:", filename)
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                lines = [line.replace("Oak Park", "OakPark") for line in lines]
                
            tuple_data = []
            for line in lines:
                line = re.sub(r'\s+', '\t', line.strip())
                parts = line.split('\t')

                parts = [normalize_station_name(p) for p in parts if p.strip()]

                a, b = parts
                tuple_data.append((a, b))

            new_edges = clean_duplicates(tuple_data)

            if df_edges.empty:
                for a, b in new_edges:
                    a_mapped = fuzzy_match(a, dict_key.keys())
                    b_mapped = fuzzy_match(b, dict_key.keys())

                    if a_mapped and b_mapped:
                        mapped_edge = (dict_key[a_mapped], dict_key[b_mapped])
                        df_edges = add_record(df_edges, mapped_edge, 0000)
                    
                old_edges = new_edges
            else:
                mapped_new_edges = []
                for a, b in new_edges:
                    a_mapped = fuzzy_match(a, dict_key.keys())
                    b_mapped = fuzzy_match(b, dict_key.keys())

                    if a_mapped and b_mapped:
                        mapped_edge = (dict_key[a_mapped], dict_key[b_mapped])
                        mapped_new_edges.append(mapped_edge)
                    
                unique_new_edges = [edge for edge in mapped_new_edges if edge not in old_edges]

                for edge in unique_new_edges:
                    df_edges = add_record(df_edges, edge, 0000)

                if unique_new_edges:
                    old_edges.extend(unique_new_edges)


    #mark year as unknwon
    df_edges['year'] = df_edges['year'].replace(0, 'unknown')


    return df_edges, dict_key



def name_to_ID(stations_grouped, dict_key):
   
    valid_names = list(dict_key.keys())
    converted = {}

    for line_name, station_list in stations_grouped.items():
        converted[line_name] = []
        for station in station_list:
            station_id = dict_key.get(station, -1)
            if station_id == -1:
                best_match = fuzzy_match(station, valid_names)
                if best_match:
                    station_id = dict_key[best_match]
                else:
                    print(f"Unmatched station: {station}")
            if station_id != -1:
                converted[line_name].append(station_id)
    
    return converted




def get_lines_from_file(filename, dict_key, city_path = "./Berlin", file_prefix = "berlin-", file_suffix = ".txt", line_prefixes=None,more_files=False, separator = True):
    if more_files and line_prefixes is None:
        raise ValueError("If more_files=True, line_prefixes must be provided.")

    if line_prefixes is None:
        line_prefixes = ["Line"]

    if more_files:
        files = []
        ordered_stations = []
        for keyword in line_prefixes:
            pattern = os.path.join(city_path, f"{file_prefix}{keyword}*{file_suffix}")
            print(pattern)
            files.extend(glob.glob(pattern))


        files = sorted(files)  # Sort all found files

        line_names = []

        stations_grouped = {}
        for filename in files:
            print("Processing:", filename)
            
            #add line name to the list
            basename = os.path.basename(filename)
            if separator:
                line_name = basename.split("-")[1]
                line_name = line_name.split(".")[0]
                line_names.append(line_name)
            else:
                line_name = basename.split(".")[0] 
                line_names.append(line_name)

            stations_per_line = []

            with open(filename, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                #Replace problematic line:
                for line in lines:
                    lines = [line.replace("Oak Park", "OakPark") for line in lines]
                
                for line in lines:
                    line_edges = line.strip().split()
                    stations_per_line.append(line_edges)
                
                stations_per_line = np.array([station for edge in stations_per_line for station in edge])
                
                #add to dictionary and remove duplicates
                #_, idx = np.unique(stations_per_line, return_index=True)
                #stations_per_line = stations_per_line[np.sort(idx)]


                stations_grouped[line_name] = stations_per_line

        stations_grouped = pd.Series(stations_grouped)
        stations_grouped[0] = stations_grouped[0][stations_grouped[0] != 'Roosevel']

        stations_grouped = name_to_ID(stations_grouped, dict_key)

        return stations_grouped
    
    else :
        stations = []
        lines = []

        with open(filename, "r", encoding="latin-1") as f:
            for line in f:
                parts = line.strip().split()
                station_name = parts[0]

                station_lines = []

                for p in parts:
                    if any(p.startswith(prefix) for prefix in line_prefixes):
                        station_lines.append(p)

                if not station_lines:
                    station_lines = [None]  # or empty list, if no line info
                
                for line_ in station_lines:
                    stations.append(station_name)
                    lines.append(line_)

        for i, name in enumerate(stations):
            if name.startswith("Av."):
                stations[i] = name.replace("Av.", "Avinguda")
            
            
        # Create DataFrame
        df_lines = pd.DataFrame({
            "Station": stations,
            "Line": lines
        })

        #clean station data

        # Step 1: Group and count unique stations per line
        station_counts = df_lines.groupby("Line")["Station"].nunique()

        # Step 2: Keep only lines with more than one station
        valid_lines = station_counts[station_counts > 1].index

        # Step 3: Filter the original DataFrame
        df_filtered = df_lines[df_lines["Line"].isin(valid_lines)]

        #group stations by line
       
        stations_grouped = df_filtered.groupby("Line")["Station"].apply(list)
        #print(stations_grouped)
        stations_grouped = name_to_ID(stations_grouped,dict_key)

        return stations_grouped

        


def assign_line_ordered(df_edges, stations_grouped):
    rows = []

    for i in range(df_edges.shape[0]):
        from_station = df_edges.iloc[i]['nodeID_from']
        to_station = df_edges.iloc[i]['nodeID_to']
        matching_lines = []

        for line_name, station_list in stations_grouped.items():
            # Check all adjacent pairs in the full station list (with duplicates)
            for j in range(len(station_list) - 1):
                a, b = station_list[j], station_list[j + 1]
                if (a == from_station and b == to_station) or (a == to_station and b == from_station):
                    matching_lines.append(line_name)
                    break  # No need to keep scanning this line
        #print(matching_lines)
        if matching_lines:
            for line in matching_lines:
                row = df_edges.iloc[i].copy()
                row['line'] = line
                rows.append(row)
        else:
            row = df_edges.iloc[i].copy()
            row['line'] = 'unknown'
            rows.append(row)

    return pd.DataFrame(rows)


def assign_line(df_edges,stations_grouped):
    # Create a list to store the line for each edge
   
    edge_lines = []

    # Iterate through each row in the edge DataFrame
    for i in range(df_edges.shape[0]):
        from_station = df_edges.iloc[i]['nodeID_from']
        to_station = df_edges.iloc[i]['nodeID_to']
        found_line = None

        # Iterate through all grouped lines
        for line_name, station_list in stations_grouped.items():
            if from_station in station_list and to_station in station_list:
                found_line = line_name
                break  # stop after finding the first matching line

        edge_lines.append(found_line)

    #print(df_edges)
    # Add the line column to the DataFrame
    df_edges['line'] = edge_lines
    #print(df_edges)
    # mark as unknwon null entries
    df_edges['line'] = df_edges['line'].fillna('unknown')  
    #print(df_edges)
    
    return df_edges




def add_labels(df_edges,dict_key):
    reversed_dict = {value: key for key, value in dict_key.items()}

    df_edges["nodeFromLabel"] = df_edges["nodeID_from"].map(reversed_dict)
    df_edges["nodeToLabel"] = df_edges["nodeID_to"].map(reversed_dict)
    #print(dict_key)

    return df_edges

def get_nodes_from_file(filename, df_edges):
    #filename = "./Barcelona/barcelona-stations-positions-years.txt"

    stations = []
    latitudes = []
    longitudes = []
    years = []

    with open(filename, "r", encoding="latin-1") as f:
        for line in f:
            parts = line.strip().split()
            #if len(parts) <= 4:
            station_name = parts[0]
            
            stations.append(parts[0])
            latitudes.append(parts[1])
            longitudes.append(parts[2])
            years.append(parts[3])

    for i, name in enumerate(stations):
        if name.startswith("Av."):
            stations[i] = name.replace("Av.", "Avinguda")
        

    # Create DataFrame
    df_nodes = pd.DataFrame({
        "nodeLabel": stations,
        "latitude": latitudes,
        "longitude": longitudes,
        "year" : years
    })

    df_nodes.insert(0, 'nodeID', df_nodes.index)
    df_nodes.loc[df_nodes["year"] == '0000', "year"] = 'unknown'

    #used_nodes = np.concatenate((df_edges["nodeID_to"].to_numpy(), df_edges["nodeID_from"].to_numpy()))
    #df_nodes = df_nodes[df_nodes["nodeID"].isin(used_nodes)]

    return df_nodes

def map_label(label, id_map, valid_labels, threshold):
    if label in id_map:
        return id_map[label]
    match = fuzzy_match(label, valid_labels, threshold)
    if match:
        return id_map[match]
    return None

def reset_ID(df_edges, df_nodes, threshold=70):
    #print('before reset id', df_edges.shape)

    df_nodes = df_nodes.reset_index(drop=True)
    df_nodes['nodeID'] = (df_nodes.index + 1).astype(int)

    id_map = df_nodes.set_index('nodeLabel')['nodeID'].to_dict()
    valid_labels = list(id_map.keys())

    df_edges['nodeID_from'] = df_edges['nodeFromLabel'].apply(
        lambda label: map_label(label, id_map, valid_labels, threshold)
    )
    df_edges['nodeID_to'] = df_edges['nodeToLabel'].apply(
        lambda label: map_label(label, id_map, valid_labels, threshold)
    )

    df_nodes = df_nodes.reset_index(drop=True)
    df_edges = df_edges.reset_index(drop=True)

    # Clean the df
    df_edges.dropna(subset=['nodeID_from', 'nodeID_to'], inplace=True)
    df_edges.drop(['nodeFromLabel', 'nodeToLabel'], axis=1, inplace=True)
    df_edges = df_edges.drop_duplicates()


    df_edges['nodeID_from'] = df_edges['nodeID_from'].astype(int)
    df_edges['nodeID_to'] = df_edges['nodeID_to'].astype(int)

    #print('after reset id', df_edges.shape)
    return df_edges, df_nodes


def save_lists(df_edges, df_nodes, filename_edges, filename_nodes):
    df_edges['line'] = df_edges['line'].apply(lambda x: x.removeprefix('mx'))

    df_edges['weight'] = 1 # since undirected networks
    df_edges.to_csv(filename_edges,index = False)
    df_nodes.to_csv(filename_nodes,index = False)



{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "05cf2f7f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np \n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import igraph as ig\n",
    "from io import StringIO\n",
    "import glob\n",
    "import os\n",
    "from helper_functions import *\n",
    "from extract_data_pipeline import *\n",
    "from extract_data_pipeline_no_topology import *"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8cd789eb",
   "metadata": {},
   "source": [
    "# Edgelist"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "4fec2855",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Processing: ./Beijing/Beijing-topologies/Beijing-1971-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1972-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1973-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1974-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1975-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1976-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1977-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1978-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1979-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1980-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1981-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1982-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1983-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1984-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1985-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1986-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1987-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1988-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1989-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1990-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1991-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1992-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1993-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1994-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1995-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1996-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1997-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1998-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1999-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2000-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2001-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2002-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2003-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2004-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2005-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2006-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2007-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2008-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2009-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2010-matrix.mat\n"
     ]
    }
   ],
   "source": [
    "file_pattern = \"./Beijing/Beijing-topologies/Beijing-*-matrix.mat\"\n",
    "df_edges, dict_key = edges_from_topology(file_pattern)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fb039cff",
   "metadata": {},
   "source": [
    "### Find the line"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "59d55800",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Line\n",
      "Line1     [Babaoshan, BajiaoAmusementPark, Dawanglu, Don...\n",
      "Line10    [AgriculturalExhibitionCenter, Anzhenmen, Bago...\n",
      "Line13    [Beiyuan, Dazhongsi, Guangximen, Huilongguan, ...\n",
      "Line15    [Cuigezhuang, Houshayu, Hualikan, Maquanying, ...\n",
      "Line2     [Andingmen, BeijingRailwayStation, Changchunji...\n",
      "Line4     [AnheqiaoNorth, Beigongmen, BeijingSouthRailwa...\n",
      "Line5     [Beixinqiao, BeiyuanluNorth, Chongwenmen, Ciqi...\n",
      "Line8     [Beitucheng, ForestParkSouthGate, OlympicGreen...\n",
      "Name: Station, dtype: object\n"
     ]
    }
   ],
   "source": [
    "filename = \"./Beijing/beijing-stations-positions-years2.txt\"\n",
    "line_prefixes = [\"Line\", \"Batong\", \"Daxing\", \"Yzhuang\", \"Changping\", \"Airport\"]  \n",
    "stations_grouped = get_lines_from_file(filename,dict_key, line_prefixes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "aca2343c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "     nodeID_from  nodeID_to  year    line\n",
      "0              4          6  1972   Line1\n",
      "1              4        157  1972   Line1\n",
      "2              6         47  1972   Line1\n",
      "3              9         21  1972   Line2\n",
      "4              9         65  1972    None\n",
      "..           ...        ...   ...     ...\n",
      "140          105        135  2010  Line13\n",
      "141          135        161  2010  Line13\n",
      "142          139        149  2010    None\n",
      "143          143        148  2010   Line4\n",
      "144          147        156  2010   Line4\n",
      "\n",
      "[145 rows x 4 columns]\n",
      "     nodeID_from  nodeID_to  year     line\n",
      "0              4          6  1972    Line1\n",
      "1              4        157  1972    Line1\n",
      "2              6         47  1972    Line1\n",
      "3              9         21  1972    Line2\n",
      "4              9         65  1972  unknown\n",
      "..           ...        ...   ...      ...\n",
      "140          105        135  2010   Line13\n",
      "141          135        161  2010   Line13\n",
      "142          139        149  2010  unknown\n",
      "143          143        148  2010    Line4\n",
      "144          147        156  2010    Line4\n",
      "\n",
      "[145 rows x 4 columns]\n"
     ]
    }
   ],
   "source": [
    "df_edges = assign_line(df_edges,stations_grouped)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "4d799898",
   "metadata": {},
   "outputs": [],
   "source": [
    "df_edges = add_labels(df_edges,dict_key)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "312576fe",
   "metadata": {},
   "source": [
    "# Nodelist"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "50f2e2cb",
   "metadata": {},
   "outputs": [],
   "source": [
    "filename = \"./Beijing/beijing-stations-positions-years.txt\"\n",
    "\n",
    "df_nodes = get_nodes_from_file(filename, df_edges)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "247eacd8",
   "metadata": {},
   "source": [
    "### Remap indices"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "b6d3f3bd",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "before reset id (145, 6)\n",
      "after reset id (145, 4)\n"
     ]
    }
   ],
   "source": [
    "df_edges, df_nodes = reset_ID(df_edges,df_nodes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "13ad5a99",
   "metadata": {},
   "outputs": [],
   "source": [
    "save_lists(df_edges, df_nodes, \"Beijing_edgelist.csv\", \"Beijing_nodelist.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "cb884047",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Processing: ./Beijing/Beijing-topologies/Beijing-1971-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1972-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1973-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1974-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1975-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1976-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1977-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1978-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1979-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1980-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1981-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1982-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1983-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1984-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1985-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1986-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1987-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1988-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1989-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1990-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1991-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1992-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1993-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1994-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1995-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1996-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1997-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1998-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-1999-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2000-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2001-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2002-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2003-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2004-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2005-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2006-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2007-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2008-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2009-matrix.mat\n",
      "Processing: ./Beijing/Beijing-topologies/Beijing-2010-matrix.mat\n",
      "Line\n",
      "Airport                    [Sanyuanqiao, Terminal2, Terminal3]\n",
      "Batong       [Baliqiao, CommunicationUniversityofChina, Gao...\n",
      "Changping    [Gonghuacheng, LifeSciencePark, Nanshao, Shahe...\n",
      "Daxing       [BiomedicalBase, GaomidianNorth, GaomidianSout...\n",
      "Line1        [Babaoshan, BajiaoAmusementPark, Dawanglu, Don...\n",
      "Line10       [AgriculturalExhibitionCenter, Anzhenmen, Bago...\n",
      "Line13       [Beiyuan, Dazhongsi, Guangximen, Huilongguan, ...\n",
      "Line15       [Cuigezhuang, Houshayu, Hualikan, Maquanying, ...\n",
      "Line2        [Andingmen, BeijingRailwayStation, Changchunji...\n",
      "Line4        [AnheqiaoNorth, Beigongmen, BeijingSouthRailwa...\n",
      "Line5        [Beixinqiao, BeiyuanluNorth, Chongwenmen, Ciqi...\n",
      "Line8        [Beitucheng, ForestParkSouthGate, OlympicGreen...\n",
      "Yzhuang                                      [Ciqu, CiquSouth]\n",
      "Name: Station, dtype: object\n",
      "     nodeID_from  nodeID_to  year    line\n",
      "0              4          6  1972   Line1\n",
      "1              4        157  1972   Line1\n",
      "2              6         47  1972   Line1\n",
      "3              9         21  1972   Line2\n",
      "4              9         65  1972    None\n",
      "..           ...        ...   ...     ...\n",
      "140          105        135  2010  Line13\n",
      "141          135        161  2010  Line13\n",
      "142          139        149  2010    None\n",
      "143          143        148  2010   Line4\n",
      "144          147        156  2010   Line4\n",
      "\n",
      "[145 rows x 4 columns]\n",
      "     nodeID_from  nodeID_to  year     line\n",
      "0              4          6  1972    Line1\n",
      "1              4        157  1972    Line1\n",
      "2              6         47  1972    Line1\n",
      "3              9         21  1972    Line2\n",
      "4              9         65  1972  unknown\n",
      "..           ...        ...   ...      ...\n",
      "140          105        135  2010   Line13\n",
      "141          135        161  2010   Line13\n",
      "142          139        149  2010  unknown\n",
      "143          143        148  2010    Line4\n",
      "144          147        156  2010    Line4\n",
      "\n",
      "[145 rows x 4 columns]\n",
      "before reset id (145, 6)\n",
      "after reset id (145, 4)\n"
     ]
    }
   ],
   "source": [
    "file_pattern_topologies = \"./Beijing/Beijing-topologies/Beijing-*-matrix.mat\"\n",
    "file_lines = \"./Beijing/beijing-stations-positions-years2.txt\"\n",
    "line_prefixes = [\"Line\", \"Batong\", \"Daxing\", \"Yzhuang\", \"Changping\", \"Airport\"]\n",
    "filename_nodes = \"./Beijing/beijing-stations-positions-years.txt\"\n",
    "output_edges = \"Beijing_edgelist.csv\"\n",
    "output_nodes = \"Beijing_nodelist.csv\"\n",
    "\n",
    "extract_data_pipeline(file_pattern_topologies, file_lines, filename_nodes, \n",
    "                      output_edges, output_nodes, line_prefixes=line_prefixes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d9cc91a9",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "python3_env",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.16"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

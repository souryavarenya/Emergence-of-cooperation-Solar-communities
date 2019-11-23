
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

# Import Visualization Functions
from VisualizationFunctions import ColourMap
from VisualizationFunctions import AnimateColourMap
from VisualizationFunctions import MultiAgentLinePlot

#%%

# Systematical naming for input and output files
curr_profile = 1                                    # Current Profile #
curr_profile_name = "profile"+str(curr_profile)     # Current Profile name

m_prof_file = "Data/"+curr_profile_name+".json"     # Current input profile

# Datalogging files
HF_data_file = "Datalogs/Logs/"+curr_profile_name+"_HF.csv"
MF_data_file = "Datalogs/Logs/"+curr_profile_name+"_MF.csv"
Coord_file = "Datalogs/Logs/Coordinates.csv"

# Read building data from the CSV
MF_data = pd.read_csv(MF_data_file, sep=';', index_col='Step')
HF_data = pd.read_csv(HF_data_file, sep=';', index_col=['Step','AgentID'])
Coords = pd.read_csv(Coord_file, sep=';', index_col=['AgentID'])

# Extract Coordinate Arrays
x_coord = Coords['x'].to_numpy()
y_coord = Coords['y'].to_numpy()

# Extract number of Steps and Number of Agents -> Last step and last agent
(n_steps, n_agents) = HF_data.index[len(HF_data.index)-1]
n_steps = int((n_steps/2)+1)    # Correct to actual number of steps
n_agents +=1

#%%
# UTILITY ANALYSIS
Utility_matrix = np.reshape(HF_data['Utility'].to_numpy(),(n_steps,n_agents))
Final_Utility = Utility_matrix[n_steps-1]

# Final Utility Color Map
ColourMap(x_coord, y_coord, Final_Utility, col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title="Final utility distribution",size=(10,5),cmap='RdYlGn',markersize=50,save=1,show=1,filename="Visualization/res/UtilityMap.svg")

# Evolution of utility .gif
AnimateColourMap(n_steps, x_coord, y_coord, Utility_matrix, dlyfactor=0.3, col_range=(0,1), x_label="", y_label="", colorbar=1, Nlegend=3, color_label=['Low (0)', '', 'High (1)'], title="Evolution of Utility", size=(10,5),cmap='RdYlGn',markersize=50,filename="Visualization/res/UtilityEvolution.gif")

# Evolution of utility for n agents
MultiAgentLinePlot(Utility_matrix, n_agents, x_axis=[], step=0, show=1, x_label="Time", y_label="Utility Value", legend=1, cmap='RdYlGn', title="Utility Evolution over time", size=(15,10), save=1, filename="Visualization/res/UtilityMultiagent.svg")

#%%
# IDEA ANALYSIS
Idea_df = MF_data[['Idea_cnt', 'Idea_chg']]

Idea_change_t = MF_data.index.to_numpy()
Idea_change_t = np.reshape(Idea_change_t, (np.size(Idea_change_t),1))
Idea_count = MF_data[['Idea_cnt']].to_numpy().transpose()
Idea_count = np.reshape(Idea_count, (np.size(Idea_count),1))

MultiAgentLinePlot(Idea_count, 1, x_axis=Idea_change_t, step=1, show=1, x_label="Time", y_label="# Nodes with the Idea", legend=1, cmap='RdYlGn', title="# Nodes with Idea over time", size=(15,10), save=1, filename="Visualization/res/IdeaCount.svg")



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

# Import Visualization Functions
from VisualizationFunctions import ColourMap
from VisualizationFunctions import AnimateColourMap
from VisualizationFunctions import MultiLinePlot
from VisualizationFunctions import HistogramPlot

# Import Analysis Functions
from AnalysisFunctions import CountVarsList
from AnalysisFunctions import ReconstructBoolMatrix
from AnalysisFunctions import AverageHFDataframe

#%%
# --------------------------------------
# READ DATA AND PREPARE GLOBAL VARIABLES
# --------------------------------------

# Systematical naming for input and output files
curr_profile = 1                                    # Current Profile #
curr_profile_name = "profile_"+str(curr_profile)     # Current Profile name

m_prof_file = "Data/"+curr_profile_name+".json"     # Current input profile

# Datalogging files
HF_data_file = "Datalogs/Logs/"+curr_profile_name+"_HF.csv"
MF_data_file = "Datalogs/Logs/"+curr_profile_name+"_MF.csv"
Coord_file = "Datalogs/Logs/Coordinates.csv"

# Read data from the CSV
MF_data = pd.read_csv(MF_data_file, sep=';', index_col=['Run','Step'])
HF_data = pd.read_csv(HF_data_file, sep=';', index_col=['Run','Step','AgentID'])
Coords = pd.read_csv(Coord_file, sep=';', index_col=['AgentID'])

# Extract Coordinate Arrays
x_coord = Coords['x'].to_numpy()
y_coord = Coords['y'].to_numpy()

# Extract Seeds
seeds = MF_data['Seed'].dropna().to_numpy()

# Extract number of Steps and Number of Agents -> Last run, last step, last agents
# IMPORTANT - We assume constant number of runs, steps and agents through the Batch
(n_runs, n_steps, n_agents) = HF_data.index[len(HF_data.index)-1]
n_steps = int((n_steps/2)+1)    # Correct to actual number (length value = last+1), steps re-scaled
n_runs +=1
n_agents +=1

# SHOW PLOTS OR NOT
show = 0

# SAVE PLOTS OR NOT
save = 1

#%%
# -------------------------
# MULTILINE EVOLUTION PLOTS
# -------------------------

# CONTINUOUS VARIABLES

run = 3

# Utility
Utility_matrix = np.reshape(HF_data['Utility'].to_numpy(),(n_runs,n_steps,n_agents))
MultiLinePlot(Utility_matrix[run], n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Utility Value", legendlabel='Agent', legend=1, cmap='RdYlGn', title="Evolution of Utility", size=(15,10), save=save, filename="Visualization/res/UtilityMultiagent.svg")

# Opinion
Opinion_matrix = np.reshape(HF_data['Opinion'].to_numpy(),(n_runs,n_steps,n_agents))
MultiLinePlot(Opinion_matrix[run], n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Opinion Value", legendlabel='Agent', legend=1, cmap='RdYlGn', title="Evolution of Opinion", size=(15,10), save=save, filename="Visualization/res/OpinionMultiagent.svg")

# Uncertainty
Uncertainty_matrix = np.reshape(HF_data['Uncertainty'].to_numpy(),(n_runs,n_steps,n_agents))
MultiLinePlot(Uncertainty_matrix[run], n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Uncertainty Value", legendlabel='Agent', legend=1, cmap='RdYlGn', title="Evolution of Uncertainty", size=(15,10), save=save, filename="Visualization/res/UncertaintyMultiagent.svg")

# DISCRETE STATE VARIABLES

runs_to_analyze = n_runs

# Evolution of #ideas over time for all runs
Idea_change_list,Idea_count_list = CountVarsList(MF_data,'Idea_cnt',runs_to_analyze,n_steps)
MultiLinePlot(Idea_count_list, runs_to_analyze, x_axis=Idea_change_list, stepshape=1, show=show, x_label="Time", y_label="# Nodes with the Idea", legendlabel='Run', legend=1, cmap='RdYlGn', title="# Nodes with Idea over time", size=(15,10), save=save, filename="Visualization/res/IdeaCount.svg")

# Evolution of #pv_alone buildings over time for all runs
PV_alone_change_list,PV_alone_count_list = CountVarsList(MF_data,'PV_alone_cnt',runs_to_analyze,n_steps)
MultiLinePlot(PV_alone_count_list, runs_to_analyze, x_axis=PV_alone_change_list, stepshape=1, show=show, x_label="Time", y_label="# Individual PV", legendlabel='Run', legend=1, cmap='RdYlGn', title="# Individual PVs over time", size=(15,10), save=save, filename="Visualization/res/PVAloneCount.svg")

# Evolution of #pv communities over time for all runs
PV_com_change_list,PV_com_count_list = CountVarsList(MF_data,'PV_com_cnt',runs_to_analyze,n_steps)
MultiLinePlot(PV_com_count_list, runs_to_analyze, x_axis=PV_com_change_list, stepshape=1, show=show, x_label="Time", y_label="# PV Communities", legendlabel='Run', legend=1, cmap='RdYlGn', title="# PV Communities over time", size=(15,10), save=save, filename="Visualization/res/CommunityCount.svg")

#%%
# ----------------------------
# FINAL AND INITIAL HISTOGRAMS
# ----------------------------

# Initial Opinion Histogram
HistogramPlot(Opinion_matrix[run,0], n_bins=25, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title="Initial Opinion Histogram", size=(15,10), save=save, filename="Visualization/res/InitialOpinionHistogram.svg")

# Final Opinion Histogram
HistogramPlot(Opinion_matrix[run,n_agents-1], n_bins=25, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title="Final Opinion Histogram", size=(15,10), save=save, filename="Visualization/res/FinalOpinionHistogram.svg")

#%%
# ----------------------------
# COLORMAPS
# ----------------------------

run = 3

# Final Utility Color Map
ColourMap(x_coord, y_coord, Opinion_matrix[run,n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title="Final utility distribution",size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/FinalUtilityMap.svg")

# Initial Opinion Color Map
ColourMap(x_coord, y_coord, Opinion_matrix[run,0], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title="Initial Opinion distribution",size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/InitialOpinionMap.svg")

# Final Opinion Color Map
ColourMap(x_coord, y_coord, Utility_matrix[run][n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title="Final Opinion distribution",size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/FinalOpinionMap.svg")


#%%
# ----------------------------
# COLORMAP ANIMATIONS
# ----------------------------

run = 6

# Reconstruct the Boolean State Matrix
Idea_M = ReconstructBoolMatrix(MF_data,'Idea_cnt','Idea_chg',run, n_steps, n_agents)
IndPV_M = ReconstructBoolMatrix(MF_data,'PV_alone_cnt','PV_alone_chg',run, n_steps, n_agents)
ComPV_M = ReconstructBoolMatrix(MF_data,'PV_com_cnt','PV_com_chg',run, n_steps, n_agents)

# PV Installation Matrix: {0-> No PV, 1-> Individual, 2-> Community}
Total_PV_M = IndPV_M + ComPV_M*2

# Create animations
AnimateColourMap(n_steps, x_coord, y_coord, Idea_M, dlyfactor=0.4, col_range=(0,1), x_label="", y_label="", colorbar=0, Nlegend=2, color_label=['No Idea', 'Idea'], title="Idea Spread", size=(10,5),cmap='RdYlGn',markersize=50,filename="Visualization/res/IdeaEvolution.gif")
AnimateColourMap(n_steps, x_coord, y_coord, Total_PV_M, dlyfactor=0.4, col_range=(0,2), x_label="", y_label="", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'], title="Evolution of PV Installations", size=(10,5),cmap='RdYlGn',markersize=50,filename="Visualization/res/PVEvolution.gif")

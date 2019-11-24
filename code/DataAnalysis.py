
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

# Import Visualization Functions
from Visualization.VisualizationFunctions import ColourMap
from Visualization.VisualizationFunctions import AnimateColourMap
from Visualization.VisualizationFunctions import MultiLinePlot
from Visualization.VisualizationFunctions import HistogramPlot

# Import Analysis Functions
from Visualization.AnalysisFunctions import CountVarsList
from Visualization.AnalysisFunctions import CountVarsAverage
from Visualization.AnalysisFunctions import ReconstructBoolMatrix
from Visualization.AnalysisFunctions import AverageHFDataframe

# Import Datalogging Functions
from Datalogs.DataloggingFunctions import ReadCSVBatch

#%%
# -----------------------------------------
# OPTIONS - Use these to control the Script
# -----------------------------------------

# SHOW PLOTS?
show = True

# SAVE PLOTS?
save = True

# COMPARE BATCHES?
batch_comparison = True

# ANALYZE SIGNE BATCH?
single_batch = True
batch_2_analyze = 3

# => Make continuous data plots? (Utility, etc)
continuous = True
# => Make state data plots? (PV alone, etc)
states = True
# => Make histograms? (PV alone, etc)              
histograms = True

# => Make colormaps?
colormaps = True
# => Run to depict in State colormaps and Animations, from batch = batch_2_analyze       
run_2_analyze = 6
# => Make colormap animations?
animations = True

#%%

# Read a profile to initialize n_runs, n_steps and n_agents
profile = 1 
HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (profile,"profile_")

#%%

'''
***********************
Inter-Batch Comparison
***********************
'''

# --------------------------
# MULTILINE EVOLUTION PLOTS
# --------------------------

n_profiles = 5

if(batch_comparison==1):

    # Initialize continuous data matrices
    Utility_space = np.zeros((n_profiles,n_steps,n_agents))
    Opinion_space = np.zeros((n_profiles,n_steps,n_agents))
    Uncertainty_space = np.zeros((n_profiles,n_steps,n_agents))

    # Initialize counter matrices
    Avg_Idea_matrix = np.zeros((n_profiles,n_steps))
    Avg_PValone_matrix = np.zeros((n_profiles,n_steps))
    Avg_PVcom_matrix = np.zeros((n_profiles,n_steps))

    # Read CSV data and distribute it to the corresponding matrix positions
    for curr_profile in range(1,n_profiles):

        HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (curr_profile,"profile_")

        Utility_space[curr_profile,:,:] = np.reshape(HF_data['Utility'].to_numpy(),(n_steps,n_agents))
        Opinion_space[curr_profile,:,:] = np.reshape(HF_data['Opinion'].to_numpy(),(n_steps,n_agents))
        Uncertainty_space[curr_profile,:,:] = np.reshape(HF_data['Uncertainty'].to_numpy(),(n_steps,n_agents))

        Avg_Idea_matrix[curr_profile,:] = CountVarsAverage(MF_data,'Idea_cnt',n_runs,n_steps)
        Avg_PValone_matrix[curr_profile,:] = CountVarsAverage(MF_data,'PV_alone_cnt',n_runs,n_steps)
        Avg_PVcom_matrix[curr_profile,:] = CountVarsAverage(MF_data,'PV_com_cnt',n_runs,n_steps)

    # CONTINUOUS VARIABLES

    # Average the values over the agents
    Utility_avg = Utility_space.sum(axis=2)/n_agents
    Opinion_avg = Opinion_space.sum(axis=2)/n_agents
    Uncertainty_avg = Uncertainty_space.sum(axis=2)/n_agents

    # Swap axes to have (n_steps, n_profiles)
    Utility_avg = Utility_avg.transpose()
    Opinion_avg = Opinion_avg.transpose()
    Uncertainty_avg = Uncertainty_avg.transpose()

    # Plots
    MultiLinePlot(Utility_avg, n_profiles, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Utility Value", legendlabel='Profile', legend=1, cmap='RdYlGn', title="Evolution of Utility", size=(15,10), save=save, filename="Visualization/res/C_Multi_Cont_Utility.svg")
    MultiLinePlot(Opinion_avg, n_profiles, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Opinion Value", legendlabel='Profile', legend=1, cmap='RdYlGn', title="Evolution of Opinion", size=(15,10), save=save, filename="Visualization/res/C_Multi_Cont_Opinion.svg")
    MultiLinePlot(Uncertainty_avg, n_profiles, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Uncertainty Value", legendlabel='Profile', legend=1, cmap='RdYlGn', title="Evolution of Uncertainty", size=(15,10), save=save, filename="Visualization/res/C_Multi_Cont_Comparison.svg")

    # DISCRETE STATE VARIABLES

    # Swap axes to have (n_steps, n_profiles)
    Avg_Idea_matrix = Avg_Idea_matrix.transpose()
    Avg_PValone_matrix = Avg_PValone_matrix.transpose()
    Avg_PVcom_matrix = Avg_PVcom_matrix.transpose()

    # Plots
    MultiLinePlot(Avg_Idea_matrix, n_profiles, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="# Agents with the Idea", legendlabel='Profile', legend=1, cmap='RdYlGn', title="Evolution of Ideas", size=(15,10), save=save, filename="Visualization/res/C_Multi_State_Idea.svg")
    MultiLinePlot(Avg_PValone_matrix, n_profiles, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="# Individual Solar Installations", legendlabel='Profile', legend=1, cmap='RdYlGn', title="Evolution of Individual PV", size=(15,10), save=save, filename="Visualization/res/C_Multi_State_PValone.svg")
    MultiLinePlot(Avg_PVcom_matrix, n_profiles, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="# Agents with Community Solar", legendlabel='Profile', legend=1, cmap='RdYlGn', title="Evolution of Community PV", size=(15,10), save=save, filename="Visualization/res/C_Multi_State_PVcommunity.svg")

#%%

'''
***************
Batch Analysis
***************
'''

if(single_batch==1):

    # READ INPUT DATA FROM BATCH TO ANALYZE

    HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (batch_2_analyze,"profile_")

    # Move data from CSV to Matrices
    Utility_matrix = np.reshape(HF_data['Utility'].to_numpy(),(n_steps,n_agents))
    Opinion_matrix = np.reshape(HF_data['Opinion'].to_numpy(),(n_steps,n_agents))
    Uncertainty_matrix = np.reshape(HF_data['Uncertainty'].to_numpy(),(n_steps,n_agents))

    # Reconstruct the Boolean State Matrices
    Idea_M = ReconstructBoolMatrix(MF_data,'Idea_cnt','Idea_chg',run_2_analyze, n_steps, n_agents)
    IndPV_M = ReconstructBoolMatrix(MF_data,'PV_alone_cnt','PV_alone_chg',run_2_analyze, n_steps, n_agents)
    ComPV_M = ReconstructBoolMatrix(MF_data,'PV_com_cnt','PV_com_chg',run_2_analyze, n_steps, n_agents)

    # PV Installation Matrix: {0-> No PV, 1-> Individual, 2-> Community}
    Total_PV_M = IndPV_M + ComPV_M*2

    # --------------------------
    # MULTILINE EVOLUTION PLOTS
    # --------------------------

    # CONTINUOUS VARIABLES
    if(continuous==1):

        # Utility
        MultiLinePlot(Utility_matrix, n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Utility Value", legendlabel='Agent', legend=0, cmap='RdYlGn', title=("Evolution of Average Utility for different Agents on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_Cont_Utility.svg")

        # Opinion
        MultiLinePlot(Opinion_matrix, n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Opinion Value", legendlabel='Agent', legend=0, cmap='RdYlGn', title=("Evolution of Average Opinion for different Agents on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_Cont_Opinion.svg")

        # Uncertainty
        MultiLinePlot(Uncertainty_matrix, n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", y_label="Uncertainty Value", legendlabel='Agent', legend=0, cmap='RdYlGn', title=("Evolution of Average Uncertainty for different Agents on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_Cont_Uncertainty.svg")

    # DISCRETE STATE VARIABLES
    if(states==1):

        # Evolution of #ideas over time for all runs
        Idea_change_list,Idea_count_list = CountVarsList(MF_data,'Idea_cnt',n_runs,n_steps)
        MultiLinePlot(Idea_count_list, n_runs, x_axis=Idea_change_list, stepshape=1, show=show, x_label="Time", y_label="# Nodes with the Idea", legendlabel='Run', legend=0, cmap='RdYlGn', title=("# Nodes with the Idea for different runs on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_State_Idea.svg")

        # Evolution of #pv_alone buildings over time for all runs
        PV_alone_change_list,PV_alone_count_list = CountVarsList(MF_data,'PV_alone_cnt',n_runs,n_steps)
        MultiLinePlot(PV_alone_count_list, n_runs, x_axis=PV_alone_change_list, stepshape=1, show=show, x_label="Time", y_label="# Individual PV", legendlabel='Run', legend=0, cmap='RdYlGn', title=("# Individual PV for different runs on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_State_PValone.svg")

        # Evolution of #pv communities over time for all runs
        PV_com_change_list,PV_com_count_list = CountVarsList(MF_data,'PV_com_cnt',n_runs,n_steps)
        MultiLinePlot(PV_com_count_list, n_runs, x_axis=PV_com_change_list, stepshape=1, show=show, x_label="Time", y_label="# PV Communities", legendlabel='Run', legend=0, cmap='RdYlGn', title=("# PV Communities for different runs on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_State_PVcommunity.svg")

    # ----------------------------
    # FINAL AND INITIAL HISTOGRAMS
    # ----------------------------
    if(histograms==1):

        # Initial Opinion Histogram
        HistogramPlot(Opinion_matrix[0], n_bins=25, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Initial Opinion Histogram on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Hist_Opinion_Initial.svg")

        # Final Opinion Histogram
        HistogramPlot(Opinion_matrix[n_agents-1], n_bins=25, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Final Opinion Histogram on profile "+str(batch_2_analyze)), size=(15,10), save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Hist_Opinion_Final.svg")

    # ----------------------------
    # COLORMAPS
    # ----------------------------
    if(colormaps==1):

        # Final Utility Color Map
        ColourMap(x_coord, y_coord, Opinion_matrix[n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title=("Final utility distribution on profile "+str(batch_2_analyze)),size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Map_Utility_Final.svg")

        # Initial Opinion Color Map
        ColourMap(x_coord, y_coord, Opinion_matrix[0], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title=("Initial Opinion distribution on profile "+str(batch_2_analyze)),size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Map_Opinion_Initial.svg")

        # Final Opinion Color Map
        ColourMap(x_coord, y_coord, Utility_matrix[n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title=("Final Opinion distribution on profile "+str(batch_2_analyze)),size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Map_Opinion_Final.svg")

        # Final Idea Color Map
        ColourMap(x_coord, y_coord, Idea_M[n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=0, Nlegend=2, color_label=['No Idea', 'Idea'],title=("Final Idea distribution on profile "+str(batch_2_analyze))+" and run "+str(run_2_analyze),size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Map_Idea_Final.svg")

        # Final PV Installations Color Map
        ColourMap(x_coord, y_coord, Total_PV_M[n_steps-1], col_range=(0,2), x_label="x coordinate", y_label="y coordinate", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'],title=("Final PV distribution on profile "+str(batch_2_analyze))+" and run "+str(run_2_analyze),size=(10,5),cmap='RdYlGn',markersize=50,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Map_PV_Final.svg")

    # ----------------------------
    # COLORMAP ANIMATIONS
    # ----------------------------

    if(animations==1):

        # Create animations
        AnimateColourMap(n_steps, x_coord, y_coord, Idea_M, dlyfactor=0.2, col_range=(0,1), x_label="", y_label="", colorbar=0, Nlegend=2, color_label=['No Idea', 'Idea'], title="Idea Spread", size=(10,5),cmap='RdYlGn',markersize=50,filename="Visualization/res/A_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Anim_IdeaEvolution.gif")
        AnimateColourMap(n_steps, x_coord, y_coord, Total_PV_M, dlyfactor=0.2, col_range=(0,2), x_label="", y_label="", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'], title="Evolution of PV Installations", size=(10,5),cmap='RdYlGn',markersize=50,filename="Visualization/res/A_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Anim_PVEvolution.gif")


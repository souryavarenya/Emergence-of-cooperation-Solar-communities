
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

# Import Visualization Functions
from Visualization.VisualizationFunctions import ColourMap
from Visualization.VisualizationFunctions import AnimateColourMap
from Visualization.VisualizationFunctions import MultiLinePlot
from Visualization.VisualizationFunctions import MultipleSubplot
from Visualization.VisualizationFunctions import HistogramPlot

# Import Analysis Functions
from Visualization.AnalysisFunctions import CountVarsList
from Visualization.AnalysisFunctions import CountVarsMatrix
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

# Figure Size
figsize = (7,5)
mapsize = (10,5)

# COMPARE BATCHES?
batch_comparison = False
n_profiles = 5

# ANALYZE SINGLE BATCH?
single_batch = False
batch_2_analyze = 4

# => Make continuous data plots? (Utility, etc)
continuous = False
# => Make state data plots? (PV alone, etc)
states = False
# => Make histograms? (PV alone, etc)              
histograms = False
# => Make colormaps?
colormaps = False  
# => Make colormap animations?
animations = False

# => Generate presentation and report plots?
presentation_plots = True
presentation_animations = False
base_scenario = True

#%%

# Read a profile to initialize n_runs, n_steps and n_agents
profile = 1 
HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (profile,"profile_")

#%%

'''
***********************
Extract data from CSV
***********************
'''

# Initialize continuous data matrices
Utility_space = np.zeros((n_profiles,n_runs,n_steps,n_agents))
Opinion_space = np.zeros((n_profiles,n_runs,n_steps,n_agents))
Uncertainty_space = np.zeros((n_profiles,n_runs,n_steps,n_agents))

Profit_space = np.zeros((n_profiles,n_runs,n_steps,n_agents))
Neighbor_space = np.zeros((n_profiles,n_runs,n_steps,n_agents))

# Initialize counter matrices
Idea_space = np.zeros((n_profiles,n_runs,n_steps))
PValone_space = np.zeros((n_profiles,n_runs,n_steps))
PVcom_space = np.zeros((n_profiles,n_runs,n_steps))

# Read CSV data and distribute it to the corresponding matrix positions
for curr_profile in range(0,n_profiles):

    HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (curr_profile,"profile_")

    Utility_space[curr_profile,:,:,:] = np.reshape(HF_data['Utility'].to_numpy(),(n_runs,n_steps,n_agents))
    Opinion_space[curr_profile,:,:,:] = np.reshape(HF_data['Opinion'].to_numpy(),(n_runs,n_steps,n_agents))
    Uncertainty_space[curr_profile,:,:,:] = np.reshape(HF_data['Uncertainty'].to_numpy(),(n_runs,n_steps,n_agents))

    Profit_space[curr_profile,:,:,:] = np.reshape(HF_data['Profit'].to_numpy(),(n_runs,n_steps,n_agents))
    Neighbor_space[curr_profile,:,:,:] = np.reshape(HF_data['Neighbor'].to_numpy(),(n_runs,n_steps,n_agents))

    Idea_space[curr_profile,:,:] = CountVarsMatrix(MF_data,'Idea_cnt',n_runs,n_steps)
    PValone_space[curr_profile,:,:] = CountVarsMatrix(MF_data,'PV_alone_cnt',n_runs,n_steps)
    PVcom_space[curr_profile,:,:] = CountVarsMatrix(MF_data,'PV_com_cnt',n_runs,n_steps)

# GET RUNS OF INTEREST
# Average over all runs
Utility_avg_r = np.mean(Utility_space,axis=1)
Opinion_avg_r = np.mean(Opinion_space,axis=1)
Uncertainty_avg_r = np.mean(Uncertainty_space,axis=1)
Profit_avg_r = np.mean(Profit_space,axis=1)
Neighbor_avg_r = np.mean(Neighbor_space,axis=1)

# Sum of Square Deviations wrto Run
Utility_diff = np.zeros((n_profiles,n_runs,n_steps,n_agents))
for r in range(0,n_runs):
    Utility_diff[:,r,:,:] = (Utility_space[:,r,:,:] - Utility_avg_r)**2

Utility_diff = np.sum(np.sum(Utility_diff,axis=3),axis=2)
Utility_interest_runs = np.argmin(Utility_diff,axis=1)      # Runs of interest -> The ones with smallest sum of square deviations wrto Run
run_2_analyze = Utility_interest_runs[batch_2_analyze]

'''
***********************
Inter-Batch Comparison
***********************
'''

# --------------------------
# MULTILINE EVOLUTION PLOTS
# --------------------------

if(batch_comparison==1):
    # CONTINUOUS VARIABLES

    # Average the values over the agents
    Utility_avg = np.mean(Utility_avg_r,axis=2)
    Opinion_avg = np.mean(Opinion_avg_r,axis=2)
    Uncertainty_avg = np.mean(Uncertainty_avg_r,axis=2)
    Profit_avg = np.mean(Profit_avg_r,axis=2)
    Neighbor_avg = np.mean(Neighbor_avg_r,axis=2)

    # Swap axes to have (n_steps, n_profiles)
    Utility_avg = Utility_avg.transpose()
    Opinion_avg = Opinion_avg.transpose()
    Uncertainty_avg = Uncertainty_avg.transpose()
    Profit_avg = Profit_avg.transpose()
    Neighbor_avg = Neighbor_avg.transpose()

    # Plot average signal values for each batch run

    MultiLinePlot(Utility_avg, n_profiles, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, x_label="Time", y_label="Utility Value", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average Utility", size=figsize, save=save, filename="Visualization/res/C_Multi_Cont_Utility.svg")
    MultiLinePlot(Opinion_avg, n_profiles, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, x_label="Time", y_label="Opinion Value", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average Opinion", size=figsize, save=save, filename="Visualization/res/C_Multi_Cont_Opinion.svg")
    MultiLinePlot(Uncertainty_avg, n_profiles, x_axis=[], y_ax_lim=[0,0.5], stepshape=0, show=show, x_label="Time", y_label="Uncertainty Value", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average Uncertainty", size=figsize, save=save, filename="Visualization/res/C_Multi_Cont_Uncertainty.svg")
    MultiLinePlot(Profit_avg, n_profiles, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, x_label="Time", y_label="Profit Value", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average Profit", size=figsize, save=save, filename="Visualization/res/C_Multi_Cont_Profit.svg")
    MultiLinePlot(Neighbor_avg, n_profiles, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, x_label="Time", y_label="Neighbor Value", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average Neighbor Value", size=figsize, save=save, filename="Visualization/res/C_Multi_Cont_Neighbor.svg")

    # Compare time behaviour of agents for each run of interest
    Utility_Mult_Subplot = np.zeros((n_profiles,n_steps,n_agents))
    Opinion_Mult_Subplot = np.zeros((n_profiles,n_steps,n_agents))
    for p in range(0,n_profiles):
        Utility_Mult_Subplot[p] = Utility_space[p,Utility_interest_runs[p]]
        Opinion_Mult_Subplot[p] = Opinion_space[p,Utility_interest_runs[p]]

    MultipleSubplot(Utility_Mult_Subplot, n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", x_ax_lim = [], y_label="Utility", y_ax_lim = [0,1], cmap='brg', title="Utility evolution comparison on each profile, for all agents", size=figsize, save=1, filename="Visualization/res/C_Sub_Cont_Utility.svg")
    MultipleSubplot(Opinion_Mult_Subplot, n_agents, x_axis=[], stepshape=0, show=show, x_label="Time", x_ax_lim = [], y_label="Opinion", y_ax_lim = [0,1], cmap='brg', title="Opinion evolution comparison on each profile, for all agents", size=figsize, save=1, filename="Visualization/res/C_Sub_Cont_Opinion.svg")

    # DISCRETE STATE VARIABLES

    # Average over all runs
    Avg_Idea_matrix = np.mean(Idea_space,axis=1)
    Avg_PValone_matrix = np.mean(PValone_space,axis=1)
    Avg_PVcom_matrix = np.mean(PVcom_space,axis=1)

    # Swap axes to have (n_steps, n_profiles)
    Avg_Idea_matrix = Avg_Idea_matrix.transpose()
    Avg_PValone_matrix = Avg_PValone_matrix.transpose()
    Avg_PVcom_matrix = Avg_PVcom_matrix.transpose()

    # Plot average state counters for each batch run
    MultiLinePlot(Avg_Idea_matrix, n_profiles, x_axis=[], y_ax_lim=[0,550], stepshape=1, show=show, x_label="Time", y_label="# Agents with the Idea", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average # of Nodes with the Idea", size=figsize, save=save, filename="Visualization/res/C_Multi_State_Idea.svg")
    MultiLinePlot(Avg_PValone_matrix, n_profiles, x_axis=[], y_ax_lim=[0,550], stepshape=1, show=show, x_label="Time", y_label="# Individual Solar Installations", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average # of Nodes in Individual PV State", size=figsize, save=save, filename="Visualization/res/C_Multi_State_PValone.svg")
    MultiLinePlot(Avg_PVcom_matrix, n_profiles, x_axis=[], y_ax_lim=[0,550], stepshape=1, show=show, x_label="Time", y_label="# Agents with Community Solar", legendlabel='Profile', legend=1, cmap='brg', title="Evolution of Average # of Nodes in Community PV State", size=figsize, save=save, filename="Visualization/res/C_Multi_State_PVcommunity.svg")


#%%

'''
***************
Batch Analysis
***************
'''

if(single_batch==1):

    print("Analyzing run of Interest "+str(run_2_analyze)+" from batch #"+str(batch_2_analyze))

    # READ DATAFRAME FROM BATCH TO ANALYZE

    HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (batch_2_analyze,"profile_")

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
        MultiLinePlot(Utility_space[batch_2_analyze,run_2_analyze], n_agents, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, x_label="Time", y_label="Utility Value", legendlabel='Agent', legend=0, cmap='brg', title=("Evolution of Average Utility for different Agents on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_Cont_Utility.svg")

        # Opinion
        MultiLinePlot(Opinion_space[batch_2_analyze,run_2_analyze], n_agents, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, x_label="Time", y_label="Opinion Value", legendlabel='Agent', legend=0, cmap='brg', title=("Evolution of Average Opinion for different Agents on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_Cont_Opinion.svg")

        # Uncertainty
        MultiLinePlot(Uncertainty_space[batch_2_analyze,run_2_analyze], n_agents, x_axis=[], y_ax_lim=[0,0.5], stepshape=0, show=show, x_label="Time", y_label="Uncertainty Value", legendlabel='Agent', legend=0, cmap='brg', title=("Evolution of Average Uncertainty for different Agents on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_Cont_Uncertainty.svg")

    # DISCRETE STATE VARIABLES
    if(states==1):

        # Evolution of #ideas over time for all runs
        Idea_change_list,Idea_count_list = CountVarsList(MF_data,'Idea_cnt',n_runs,n_steps)
        MultiLinePlot(Idea_count_list, n_runs, x_axis=Idea_change_list, y_ax_lim=[0,550], stepshape=1, show=show, x_label="Time", y_label="# Nodes with the Idea", legendlabel='Run', legend=0, cmap='brg', title=("# Nodes with the Idea for different runs on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_State_Idea.svg")

        # Evolution of #pv_alone buildings over time for all runs
        PV_alone_change_list,PV_alone_count_list = CountVarsList(MF_data,'PV_alone_cnt',n_runs,n_steps)
        MultiLinePlot(PV_alone_count_list, n_runs, x_axis=PV_alone_change_list, y_ax_lim=[0,550], stepshape=1, show=show, x_label="Time", y_label="# Individual PV", legendlabel='Run', legend=0, cmap='brg', title=("# Individual PV for different runs on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_State_PValone.svg")

        # Evolution of #pv communities over time for all runs
        PV_com_change_list,PV_com_count_list = CountVarsList(MF_data,'PV_com_cnt',n_runs,n_steps)
        MultiLinePlot(PV_com_count_list, n_runs, x_axis=PV_com_change_list, y_ax_lim=[0,550], stepshape=1, show=show, x_label="Time", y_label="# PV Communities", legendlabel='Run', legend=0, cmap='brg', title=("# PV Communities for different runs on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Multi_State_PVcommunity.svg")

    # ----------------------------
    # FINAL AND INITIAL HISTOGRAMS
    # ----------------------------
    if(histograms==1):

        # Initial Opinion Histogram
        HistogramPlot(Opinion_space[batch_2_analyze,run_2_analyze,0], x_ax_lim=[0,1], n_bins=50, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Initial Opinion Histogram on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Hist_Opinion_Initial.svg")

        # Final Opinion Histogram
        HistogramPlot(Opinion_space[batch_2_analyze,run_2_analyze,n_steps-1], x_ax_lim=[0,1], n_bins=50, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Final Opinion Histogram on profile "+str(batch_2_analyze)), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Hist_Opinion_Final.svg")

    # ----------------------------
    # COLORMAPS
    # ----------------------------
    if(colormaps==1):

        # Final Utility Color Map
        ColourMap(x_coord, y_coord, Opinion_space[batch_2_analyze,run_2_analyze,n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title=("Final utility distribution on profile "+str(batch_2_analyze)),size=mapsize,cmap='RdYlGn',markersize=20,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Map_Utility_Final.svg")

        # Initial Opinion Color Map
        ColourMap(x_coord, y_coord, Opinion_space[batch_2_analyze,run_2_analyze,0], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title=("Initial Opinion distribution on profile "+str(batch_2_analyze)),size=mapsize,cmap='RdYlGn',markersize=20,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Map_Opinion_Initial.svg")

        # Final Opinion Color Map
        ColourMap(x_coord, y_coord, Utility_space[batch_2_analyze,run_2_analyze,n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=1, Nlegend=2, color_label=['Low (0)','', 'High (1)'],title=("Final Opinion distribution on profile "+str(batch_2_analyze)),size=mapsize,cmap='RdYlGn',markersize=20,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Map_Opinion_Final.svg")

        # Final Idea Color Map
        ColourMap(x_coord, y_coord, Idea_M[n_steps-1], col_range=(0,1), x_label="x coordinate", y_label="y coordinate", colorbar=0, Nlegend=2, color_label=['No Idea', 'Idea'],title=("Final Idea distribution on profile "+str(batch_2_analyze)),size=mapsize,cmap='RdYlGn',markersize=20,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Map_Idea_Final.svg")

        # Final PV Installations Color Map
        ColourMap(x_coord, y_coord, Total_PV_M[n_steps-1], col_range=(0,2), x_label="x coordinate", y_label="y coordinate", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'],title=("Final PV distribution on profile "+str(batch_2_analyze)),size=mapsize,cmap='RdYlGn',markersize=20,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Map_PV_Final.svg")

    # ----------------------------
    # COLORMAP ANIMATIONS
    # ----------------------------

    if(animations==1):

        # Create animations
        AnimateColourMap(n_steps, x_coord, y_coord, Idea_M, dlyfactor=0.2, col_range=(0,1), x_label="", y_label="", colorbar=0, Nlegend=2, color_label=['No Idea', 'Idea'], title="Idea Spread on profile "+str(batch_2_analyze), size=mapsize,cmap='RdYlGn',markersize=20,filename="Visualization/res/A_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Anim_IdeaEvolution.gif")
        AnimateColourMap(n_steps, x_coord, y_coord, Total_PV_M, dlyfactor=0.4, col_range=(0,2), x_label="", y_label="", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'], title="Evolution of PV Installations on profile "+str(batch_2_analyze), size=mapsize,cmap='RdYlGn',markersize=20,filename="Visualization/res/A_Profile_"+str(batch_2_analyze)+"_Run_"+str(run_2_analyze)+"_Anim_PVEvolution.gif")

#%%

# ---------------------------------------------------------
# SPECIFIC FIGURES OF INTEREST FOR REPORT AND PRESENTATION
# ---------------------------------------------------------

# -------------------------------------------------
# Plots for all batches:
#       Initial and Final Hisograms
#       Final PV Landscape
#       PV Landscape evolution

if(presentation_plots):

    #label_list = ["+20% Neg Extremists","+5% Neg Extremists","Base Scenario","+5% Pos Extremists","+20% Pos Extremists"]
    label_list = ["Base Scenario","+5% Extremists","+10% Extremists","+20% Extremists","+40% Extremists"]

    for batch in range(0,n_profiles):
        run = Utility_interest_runs[batch]

        HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (batch,"profile_")

        # Reconstruct the Boolean State Matrices
        Idea_M = ReconstructBoolMatrix(MF_data,'Idea_cnt','Idea_chg',run, n_steps, n_agents)
        IndPV_M = ReconstructBoolMatrix(MF_data,'PV_alone_cnt','PV_alone_chg',run, n_steps, n_agents)
        ComPV_M = ReconstructBoolMatrix(MF_data,'PV_com_cnt','PV_com_chg',run, n_steps, n_agents)

        # PV Installation Matrix: {0-> No PV, 1-> Individual, 2-> Community}
        Total_PV_M = IndPV_M + ComPV_M*2

        '''
        HistogramPlot(Opinion_space[batch,run,0], x_ax_lim=[0,1], n_bins=50, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Initial Opinion with "+label_list[batch]), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch)+"_Hist_Opinion_Initial_PRESENTATION.svg")
        HistogramPlot(Opinion_space[batch,run,n_steps-1], x_ax_lim=[0,1], n_bins=50, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Final Opinion with "+label_list[batch]), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch)+"_Hist_Opinion_Final_PRESENTATION.svg")
        
        ColourMap(x_coord, y_coord, Total_PV_M[n_steps-1], col_range=(0,2), x_label="x coordinate", y_label="y coordinate", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'],title=("Final PV landscape with "+label_list[batch]),size=mapsize,cmap='RdYlGn',markersize=20,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch)+"_Map_PV_Final_PRESENTATION.svg")
        
        if(presentation_animations):
            AnimateColourMap(n_steps, x_coord, y_coord, Total_PV_M, dlyfactor=0.2, col_range=(0,2), x_label="", y_label="", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'], title="PV landscape with "+label_list[batch], size=mapsize,cmap='RdYlGn',markersize=20,filename="Visualization/res/A_Profile_"+str(batch)+"_Anim_PVEvolution_PRESENTATION.gif")
            AnimateColourMap(n_steps, x_coord, y_coord, Utility_space[batch,run], dlyfactor=0.2, col_range=(0,1), x_label="", y_label="", colorbar=1, Nlegend=2, color_label=['Lowest (0)','Idea Threshold','Highest (1)'], title="Utility values with "+label_list[batch], size=mapsize,cmap='RdYlGn',markersize=20,filename="Visualization/res/A_Profile_"+str(batch)+"_Anim_Utility_PRESENTATION.gif")
        '''

    # -------------------------------------------------
    # Big comparative subplots:
    #       Utility evolution for particular runs
    #       Opinion evolution for particular runs

    # Compare time behaviour of agents for each run of interest
    Utility_Mult_Subplot = np.zeros((n_profiles,n_steps,n_agents))
    Opinion_Mult_Subplot = np.zeros((n_profiles,n_steps,n_agents))
    for p in range(0,n_profiles):
        Utility_Mult_Subplot[p] = Utility_space[p,Utility_interest_runs[p]]
        Opinion_Mult_Subplot[p] = Opinion_space[p,Utility_interest_runs[p]]

    MultipleSubplot(Utility_Mult_Subplot, n_agents, testvar=1, x_axis=[], stepshape=0, show=show, subtitles=label_list, x_label="Time", x_ax_lim = [], y_label="Utility", y_ax_lim = [0,1], cmap='brg', title="Utility evolution comparison on each profile, for all agents", size=figsize, save=1, alpha=0.2, filename="Visualization/res/C_Sub_Cont_Utility_PRESENTATION.svg")
    MultipleSubplot(Opinion_Mult_Subplot, n_agents, testvar=1, x_axis=[], stepshape=0, show=show, subtitles=label_list, x_label="Time", x_ax_lim = [], y_label="Opinion", y_ax_lim = [0,1], cmap='brg', title="Opinion evolution comparison on each profile, for all agents", size=figsize, save=1, alpha=0.2, filename="Visualization/res/C_Sub_Cont_Opinion_PRESENTATION.svg")

    # -------------------------------------------------
    # Average behaviour subplots:
    #       Average utility evolution
    #       Average opinion evolution
    #       Average # of nodes with PV installation
    #       Average # of nodes with PV Community

    # Average the values over the agents
    Utility_avg = np.mean(Utility_avg_r,axis=2)
    Opinion_avg = np.mean(Opinion_avg_r,axis=2)
    # Average over all runs
    Avg_PValone_matrix = np.mean(PValone_space,axis=1)
    Avg_PVcom_matrix = np.mean(PVcom_space,axis=1)

    # Swap axes to have (n_steps, n_profiles)
    Utility_avg = Utility_avg.transpose()
    Opinion_avg = Opinion_avg.transpose()
    Avg_PValone_matrix = Avg_PValone_matrix.transpose()
    Avg_PVcom_matrix = Avg_PVcom_matrix.transpose()

    # Plot average signal values for each batch run

    MultiLinePlot(Utility_avg, n_profiles, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, custom_labels=label_list, x_label="Time", y_label="Utility Value", legend=1, cmap='brg', title="Average Utility Signal", size=figsize, save=save, filename="Visualization/res/C_Multi_Cont_Utility_PRESENTATION.svg")
    MultiLinePlot(Opinion_avg, n_profiles, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, custom_labels=label_list, x_label="Time", y_label="Opinion Value", legend=1, cmap='brg', title="Average Opinion Signal", size=figsize, save=save, filename="Visualization/res/C_Multi_Cont_Opinion_PRESENTATION.svg")

    ''' REVIEW - CHANGE BY PROPER PLOTS '''
    '''
    MultiLinePlot(Avg_PValone_matrix, n_profiles, x_axis=[], y_ax_lim=[0,550], stepshape=1, show=show, custom_labels=label_list, x_label="Time", y_label="# Individual Solar Installations", legend=1, cmap='brg', title="Average Nodes with Individual PV", size=figsize, save=save, filename="Visualization/res/C_Multi_State_PValone_PRESENTATION.svg")
    MultiLinePlot(Avg_PVcom_matrix, n_profiles, x_axis=[], y_ax_lim=[0,550], stepshape=1, show=show, custom_labels=label_list, legendpos='upper right', x_label="Time", y_label="# Agents with Community Solar", legend=1, cmap='brg', title="Average Nodes with Community PV", size=figsize, save=save, filename="Visualization/res/C_Multi_State_PVcommunity_PRESENTATION.svg")
    '''
    # ---------------------------------------------------------
    # SPECIFIC FIGURES OF INTEREST FOR REPORT - BASELINE CASE
    # ---------------------------------------------------------

    if(base_scenario):

        # Average the values over the agents
        Profit_avg = np.mean(Profit_avg_r,axis=2)
        Neighbor_avg = np.mean(Neighbor_avg_r,axis=2)

        # Swap axes to have (n_steps, n_profiles)
        Profit_avg = Profit_avg.transpose()
        Neighbor_avg = Neighbor_avg.transpose()

        HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds = ReadCSVBatch (0,"profile_")

        # Reconstruct the Boolean State Matrices
        Idea_M = ReconstructBoolMatrix(MF_data,'Idea_cnt','Idea_chg',run, n_steps, n_agents)
        IndPV_M = ReconstructBoolMatrix(MF_data,'PV_alone_cnt','PV_alone_chg',run, n_steps, n_agents)
        ComPV_M = ReconstructBoolMatrix(MF_data,'PV_com_cnt','PV_com_chg',run, n_steps, n_agents)

        # PV Installation Matrix: {0-> No PV, 1-> Individual, 2-> Community}
        Total_PV_M = IndPV_M + ComPV_M*2

        figsize = (7,5)
        mapsize = (10,5)

        MultipleSubplot(np.array([Opinion_space[0,Utility_interest_runs[0]],Profit_space[0,Utility_interest_runs[0]],Neighbor_space[0,Utility_interest_runs[0]]]), n_agents, testvar=2, x_axis=[], stepshape=0, show=show, subtitles=["Opinion","Profit","Neighbor"], x_label="Time", x_ax_lim = [], y_label="Value", y_ax_lim = [0,1], cmap='brg', title="", size=(10,4), save=1, alpha=0.2, filename="Visualization/res/C_Sub_Cont_All_Base_PRESENTATION.svg")
        MultiLinePlot(Utility_space[0,Utility_interest_runs[0]], n_agents, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, custom_labels=label_list, x_label="Time", y_label="Utility Value", legend=0, cmap='brg', title="Utility Signal for all Agents", alpha=0.2, size=figsize, save=save, filename="Visualization/res/C_Single_Cont_Utility_Base_PRESENTATION.svg")

        MultipleSubplot(np.array([Opinion_avg,Profit_avg,Neighbor_avg]), 1, testvar=2, x_axis=[], stepshape=0, show=show, subtitles=["Opinion","Profit","Neighbor"], x_label="Time", x_ax_lim = [], y_label="Value", y_ax_lim = [0,1], cmap='brg', title="", size=(10,4), save=1, alpha=1, filename="Visualization/res/C_Sub_Cont_Avg_Base_PRESENTATION.svg")
        MultiLinePlot(Utility_avg, 1, x_axis=[], y_ax_lim=[0,1], stepshape=0, show=show, custom_labels=label_list, x_label="Time", y_label="Utility Value", legend=0, cmap='RdBu', title="Average Utility Signal", size=figsize, alpha=1, save=save, filename="Visualization/res/C_Single_Cont_AvgUtility_Base_PRESENTATION.svg")

        MultiLinePlot(Avg_PValone_matrix, 1, x_axis=[], y_ax_lim=[0,550], stepshape=1, show=show, custom_labels=label_list, x_label="Time", y_label="# Individual Solar Installations", legend=0, cmap='RdBu', title="Average Nodes with Individual PV", alpha=1, size=figsize, save=save, filename="Visualization/res/C_Single_State_PValone_Base_PRESENTATION.svg")
        MultiLinePlot(Avg_PVcom_matrix, 1, x_axis=[], y_ax_lim=[0,550], stepshape=1, show=show, custom_labels=label_list, legendpos='upper right', x_label="Time", y_label="# Agents with Community Solar", legend=0, cmap='RdBu', title="Average Nodes with Community PV", alpha=1, size=figsize, save=save, filename="Visualization/res/C_Single_State_PVcommunity_Base_PRESENTATION.svg")

        MultipleSubplot(np.array([Avg_PValone_matrix,Avg_PVcom_matrix]), 1, testvar=2, x_axis=[], stepshape=0, show=show, subtitles=["Average Nodes with Individual PV","Average Nodes with Community PV","Neighbor"], x_label="Time", x_ax_lim = [], y_label="# Agents", y_ax_lim = [0,550], cmap='brg', title="", size=(10,4), save=1, alpha=1, filename="Visualization/res/C_Sub_States_All_Base_PRESENTATION.svg")

        HistogramPlot(Opinion_space[0,Utility_interest_runs[0],0], x_ax_lim=[0,1], n_bins=50, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Initial Opinion of a representative run"), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch)+"_Hist_Opinion_Initial_Base_PRESENTATION.svg")
        HistogramPlot(Opinion_space[0,Utility_interest_runs[0],n_steps-1], x_ax_lim=[0,1], n_bins=50, show=show, x_label="Opinion value", y_label="Frequency", cmap='RdYlGn', title=("Final Opinion of a representative run"), size=figsize, save=save, filename="Visualization/res/B_Profile_"+str(batch)+"_Hist_Opinion_Final_Base_PRESENTATION.svg")

        ColourMap(x_coord, y_coord, Total_PV_M[n_steps-1], col_range=(0,2), x_label="x coordinate", y_label="y coordinate", colorbar=0, Nlegend=3, color_label=['No PV', 'Individual PV', 'PV Community'],title=("Final PV landscape of a representative run"),size=mapsize,cmap='RdYlGn',markersize=20,save=save,show=show,filename="Visualization/res/B_Profile_"+str(batch)+"_Map_PV_Final_Base_PRESENTATION.svg")

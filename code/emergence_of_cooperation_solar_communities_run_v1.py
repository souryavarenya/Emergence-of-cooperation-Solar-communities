# -*- coding: utf-8 -*-
"""
Created on November, 2019

@authors: anunezji, JFornt, marius-ethz, souryavarenya,
"""
#%%
### Import packages

# Import packages from standard library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import classes from model code
from emergence_of_cooperation_solar_communities_v1 import *

# Import functions from Visualization code
from VisualizationFunctions import *

#%%
### Collect data and set model parameters

# Define number of agents
n_agents = 3

# Define number of time steps each model runs
n_steps = 10

# Name of csv file containing data on individual buildings
b_data_file = "buildings_data.csv"

# Read data into pandas dataframe
b_data = pd.read_csv(b_data_file, nrows=n_agents)

# From the data, calculate the dimensions of the neighborhood
min_x = min(b_data["building_coord_x"])
max_x = max(b_data["building_coord_x"])
min_y = min(b_data["building_coord_y"])
max_y = max(b_data["building_coord_y"])

hood_width = int(round(max_x - min_x)) + 1
hood_height = int(round(max_y - min_y)) + 1

# Compute new coordinates for agents in the model
b_data["xcoord"] = b_data["building_coord_x"] - min_x
b_data["ycoord"] = b_data["building_coord_y"] - min_y

# Round the coordinates and make them integers so they refer to one cell
b_data["xcoord"] = b_data["xcoord"].round().astype(int)
b_data["ycoord"] = b_data["ycoord"].round().astype(int)

#%%
### VISUALIZATION VARIABLES

#Example of arrays that will contain data wrto time and agent
profit_array = np.zeros([n_steps+1,n_agents])
idea_array = np.zeros([n_steps+1,n_agents])
utility_array = np.zeros([n_steps+1,n_agents])

#%%
### RUN MODEL

model = BuildingModel(b_data, n_agents, hood_width, hood_height)

#Get initial data of interest
for i in range(0,n_agents):
    profit_array[0,i] = model.agent_list[i].profit
    idea_array[0,i] = float(model.agent_list[i].idea)
    utility_array[0,i] = model.agent_list[i].utility

for timestep in range(n_steps):
        
    model.step()
    
    #Get current data of interest
    for i in range(0,n_agents):
        profit_array[1+timestep,i] = model.agent_list[i].profit
        idea_array[1+timestep,i] = float(model.agent_list[i].idea)
        utility_array[1+timestep,i] = model.agent_list[i].utility
    
#%%
#    
### DATA VISUALIZATION WITH MATPLOTLIB-BASED FUNCTIONS

#Final Idea ColourMap
ColourMap(model.x_coord, model.y_coord, idea_array[n_steps], col_range=(0,1), x_label="", y_label="", colorbar=0, Nlegend=2, color_label=['No idea', 'Idea'], title="Final idea distribution", size=(10,5),cmap='RdYlGn',markersize=50,save=0,filename="IdeaMap.svg")

#Evolution of profit .gif
AnimateColourMap(n_steps, model.x_coord, model.y_coord, profit_array, dlyfactor=3, col_range=(0,2), x_label="", y_label="", colorbar=1, Nlegend=3, color_label=['Low', '', 'High'], title="Evolution of Profit", size=(10,5),cmap='RdYlGn',markersize=50,filename="ProfitEvolution.gif")
AnimateColourMap(n_steps, model.x_coord, model.y_coord, utility_array, dlyfactor=3, col_range=(0.6,0.9), x_label="", y_label="", colorbar=1, Nlegend=3, color_label=['Low', '', 'High'], title="Evolution of Utility", size=(10,5),cmap='RdYlGn',markersize=50,filename="Utility.gif")        

#### DATA VISUALIZATION OF GRID
#  
#
#agent_counts = np.zeros((model.grid.width, model.grid.height))
#for cell in model.grid.coord_iter():
#    cell_content, x, y = cell
#    agent_count = len(cell_content)
#    agent_counts[x][y] = agent_count
#plt.imshow(agent_counts, interpolation='nearest')
#plt.colorbar()
#
##%%
#
#### Get data from the DataCollector 
#
## for 1 measurement per step
#gini = model.datacollector.get_model_vars_dataframe()
#gini.plot()
#
## for multiple agents
#agent_wealth = model.datacollector.get_agent_vars_dataframe()
#agent_wealth.head()
#
#end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
#end_wealth.hist(bins=range(agent_wealth.Wealth.max()+1))
#
## for one agent out of out entire class
#one_agent_wealth = agent_wealth.xs(14, level="AgentID")
#one_agent_wealth.Wealth.plot()
#
##%%
#
#### BATCH RUNNER
#from mesa.batchrunner import BatchRunner
#
#fixed_params = {
#    "width": 10,
#    "height": 10
#}
#
#variable_params = {"N": range(10, 500, 10)}
#
## The variables parameters will be invoke along with the fixed parameters 
## allowing for either or both to be honored.
#batch_run = BatchRunner(
#    MoneyModel,
#    variable_params,
#    fixed_params,
#    iterations=5,
#    max_steps=100,
#    model_reporters={"Gini": compute_gini}
#)
#
#batch_run.run_all()
#
##%% 
#
#### COLLECT BATCH DATA
#
#run_data = batch_run.get_model_vars_dataframe()
#run_data.head()
#plt.scatter(run_data.N, run_data.Gini)












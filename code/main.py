### Team Red Panda
# - Fornt Mas, Jordi
# - Kovvali, Sourya
# - Nuñez-Jimenez, Alejandro
# - Schwarz, Marius

# Standard Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

# Importing the Agent and Model Classes
from Agent.BuildingAgent import BuildingAgent
from Model.BuildingModel import BuildingModel

# Import Visualization Functions
from Visualization.VisualizationFunctions import ColourMap
from Visualization.VisualizationFunctions import AnimateColourMap

# Import Datalogging Functions
from Datalogs.DataloggingFunctions import InitializeCSV
from Datalogs.DataloggingFunctions import Write2CSV

### Setting up some parameters for initialization
# Define number of agents
n_agents = 23

# Define number of time steps each model runs
n_steps = 65

# Name of csv file containing data on individual buildings
b_data_file = "Data/buildings_data.csv"
m_data_file = "Data/meta.json"

# Systematical naming for input and output files
curr_profile = 1                                    # Current Profile #
curr_profile_name = "profile"+str(curr_profile)     # Current Profile name

m_prof_file = "Data/"+curr_profile_name+".json"     # Current input profile

# Datalogging files
HF_out_file = "Datalogs/Logs/"+curr_profile_name+"_HF.csv"
MF_out_file = "Datalogs/Logs/"+curr_profile_name+"_MF.csv"
Building_Coord_file = "Datalogs/Logs/Coordinates.csv"

HF_data_columns = ['AgentID','Run','Utility','Opinion','Uncertainty']
MF_data_columns = ['Run','PV_alone_cnt','PV_alone_chg','PV_com_cnt','PV_com_chg','Idea_cnt','Idea_chg','Seed']
Building_Coord_columns = ['x','y']

# Read building data from the CSV %%file
b_data = pd.read_csv(b_data_file, nrows=n_agents)

# Read building meta data off JSON file
with open(m_data_file) as myjson:
    data_dict = json.loads(myjson.read())

# Reads the profile file and appends it to data_dict
with open(m_prof_file) as myjson:
    data_dict.update(json.loads(myjson.read()))

# Init model
model = BuildingModel(BuildingAgent, b_data, n_agents, data_dict)

# Get coordinates
x_coord = model.x_coord
y_coord = model.y_coord

# Create dataframe and write coordinates to csv file
coord_dataframe = pd.DataFrame(data={'x': x_coord, 'y': y_coord})
coord_dataframe.index.name = 'AgentID'                                         # The main index must also have a name!
coord_dataframe.to_csv(Building_Coord_file, sep=';', mode='w', header=True)    # Write dataframe to CSV, with header and in write mode

# Initialize CSV Outputs - Once per batch
InitializeCSV(HF_out_file,HF_data_columns)
InitializeCSV(MF_out_file,MF_data_columns)

batch_size = 8

# Batch of batch_size runs (PROVISIONAL, FOR TESTING)

for run in range(0,batch_size):

    # Re-Initialize model
    model = BuildingModel(BuildingAgent, b_data, n_agents, data_dict)

    # Run n_steps
    for timestep in range(n_steps):
        model.step()

    # Get Data Collector Data - Once per run
    dataframe = model.datacollector.get_agent_vars_dataframe()

    # Write data of interest to csv files - Once per run
    Write2CSV(HF_out_file,HF_data_columns,dataframe,run,n_steps,n_agents,df_type='HF')
    Write2CSV(MF_out_file,MF_data_columns,dataframe,run,n_steps,n_agents,df_type='MF')

### Results and graphs -> DataAnalysis.py

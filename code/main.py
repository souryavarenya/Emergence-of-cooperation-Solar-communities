########## Team Red Panda ###########
# - Fornt Mas, Jordi                #
# - Kovvali, Sourya                 #
# - Nuñez-Jimenez, Alejandro        #
# - Schwarz, Marius                 #
#####################################

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

# Import Analysis Functions
from Visualization.AnalysisFunctions import AverageHFDataframe

#%%

# Name of files containing initialization data
b_data_file = "Data/buildings_data_1.csv"
m_data_file = "Data/meta_1.json"

# Read building meta data off JSON file
with open(m_data_file) as myjson:
    data_dict = json.loads(myjson.read())

### Setting up some parameters for initialization
# Define number of agents
n_agents = data_dict['total_num_buildings']

# Define number of time steps each model runs -> 12 months * 10 years
#n_steps = 12*10
n_steps = 175

#HF_data_columns = ['Run',Utility','Opinion','Uncertainty']
HF_data_columns = ['Run','Utility','Opinion','Uncertainty','Neighbor','Profit']
MF_data_columns = ['Run','PV_alone_cnt','PV_alone_chg','PV_com_cnt','PV_com_chg','Idea_cnt','Idea_chg','Seed']

Building_Coord_columns = ['x','y']

# Read building data from the CSV %%file
b_data = pd.read_csv(b_data_file, nrows=n_agents)

#%%

# ITERATE OVER ALL PROFILES OF THE EXPERIMENT
n_profiles = 2

for curr_profile in range(0,n_profiles):

    print("****************************************")
    print(" RUNNING PROFILE "+str(curr_profile)+"...")
    print("****************************************")

    # Systematical naming for input and output files                                 
    curr_profile_name = "profile_"+str(curr_profile)    # Current Profile name
    m_prof_file = "Data/"+curr_profile_name+".json"     # Current input profile

    # Read building meta data off JSON file
    with open(m_data_file) as myjson:
        data_dict = json.loads(myjson.read())

    # Reads the profile file and appends it to data_dict
    with open(m_prof_file) as myjson:
        data_dict.update(json.loads(myjson.read()))

    # Initialize model
    model = BuildingModel(BuildingAgent, b_data, n_agents, data_dict)

    # Get coordinates
    x_coord = model.x_coord
    y_coord = model.y_coord

    # Datalogging files
    HF_out_file = "Datalogs/Logs/"+curr_profile_name+"_HF.csv"
    MF_out_file = "Datalogs/Logs/"+curr_profile_name+"_MF.csv"
    Building_Coord_file = "Datalogs/Logs/Coordinates.csv"

    # Create dataframe and write coordinates to csv file
    coord_dataframe = pd.DataFrame(data={'x': x_coord, 'y': y_coord})
    coord_dataframe.index.name = 'AgentID'                                         # The main index must also have a name!
    coord_dataframe.to_csv(Building_Coord_file, sep=';', mode='w', header=True)    # Write dataframe to CSV, with header and in write mode

    # Initialize CSV Outputs - Once per batch
    InitializeCSV(HF_out_file,HF_data_columns,['Step','AgentID'])
    InitializeCSV(MF_out_file,MF_data_columns,['Step'])

    batch_size = 50

    # Batch of batch_size runs

    for run in range(0,batch_size):

        #Seed
        seed = 123456789

        # Re-Initialize model
        model = BuildingModel(BuildingAgent, b_data, n_agents, data_dict)

        # Run n_steps
        for timestep in range(n_steps):
            model.step()

        # Get Data Collector Data - Once per run
        dataframe = model.datacollector.get_agent_vars_dataframe()

        # Write data of interest to MF csv files - Once per run
        Write2CSV(MF_out_file,MF_data_columns,dataframe,run,n_steps,n_agents,df_type='MF')
        Write2CSV(HF_out_file,HF_data_columns,dataframe,run,n_steps,n_agents,df_type='HF')

### Results and graphs -> DataAnalysis.py

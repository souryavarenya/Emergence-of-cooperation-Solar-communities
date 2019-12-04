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
import json, time, multiprocessing, sys, os

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

###############################################################################################

# Read the expt name from command line arguments (mandatory!)
try:
    expt_name = sys.argv[1]
except:
    print("Need to enter the experiment name")
    print("Example - uni_extremism, dual_extremism,.. ")
    sys.exit()

# Read experiment data
expt_file = "Data/Experiments/" + expt_name + ".json"
with open(expt_file) as myjson:
    expt_data = json.loads(myjson.read())

# Files of building data and the meta data
b_data_file = "Data/buildings_data.csv"
m_data_file = "Data/buildings_meta.json"

# Read building meta data from JSON file
with open(m_data_file) as myjson:
    data_dict = json.loads(myjson.read())

### Setting up some parameters for initialization
# Define number of agents
n_agents = data_dict['total_num_buildings']

# Define number of time steps each model runs -> 12 years 6 months (arbitrary)
n_steps = expt_data["n_time_steps"]

# Defining csv keys
HF_data_columns = ['Run','Utility','Opinion','Uncertainty','Neighbor','Profit']
MF_data_columns = ['Run','PV_alone_cnt','PV_alone_chg','PV_com_cnt','PV_com_chg','Com_Idea_cnt','Com_Idea_chg','Seed']

# Read building data from the CSV %%file
b_data = pd.read_csv(b_data_file, nrows=n_agents)

################################################################################################

# Function for running each profile - to be called from multiprocessing
def run_profile(expt_data, profile_id):

    start_time = time.time()
    print("****************************************")
    print(" RUNNING PROFILE " + str(profile_id) + " OF " + expt_data["experiment_name"])
    print("****************************************")

    # Systematical naming for input and output files                                 
    curr_profile_name = "profile_"+str(profile_id)    # Current Profile name
    m_prof_file = "Data/Experiments/" + expt_data["rel_profile_dir"] + "/" + curr_profile_name+".json"     
    # Current input profile

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
    log_dir = "Datalogs/Logs/"+expt_data["experiment_name"]
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    HF_out_file = log_dir + "/" + curr_profile_name + "_HF.csv"
    MF_out_file = log_dir + "/" + curr_profile_name + "_MF.csv"
    Building_Coord_file = log_dir + "/" + curr_profile_name + "_Coordinates.csv"

    # Create dataframe and write coordinates to csv file
    coord_dataframe = pd.DataFrame(data={'x': x_coord, 'y': y_coord})
    coord_dataframe.index.name = 'AgentID'                                         # The main index must also have a name!
    coord_dataframe.to_csv(Building_Coord_file, sep=';', mode='w', header=True)    # Write dataframe to CSV, with header and in write mode

    # Initialize CSV Outputs - Once per batch
    InitializeCSV(HF_out_file,HF_data_columns,['Step','AgentID'])
    InitializeCSV(MF_out_file,MF_data_columns,['Step'])

    batch_size = expt_data["n_batches"]

    try:
        myseeds = expt_data["batch_seeds"]
    except:
        myseeds = None

    # Batch of batch_size runs

    for run in range(batch_size):

        # Seed if defined in expt file
        cur_seed = myseeds[run] if myseeds != None else None

        # Re-Initialize model
        model = BuildingModel(BuildingAgent, b_data, n_agents, data_dict, seed = cur_seed)

        # Run n_steps
        for timestep in range(n_steps):
            model.step()

        # Get Data Collector Data - Once per run
        dataframe = model.datacollector.get_agent_vars_dataframe()

        # Write data of interest to MF csv files - Once per run
        Write2CSV(MF_out_file,MF_data_columns,dataframe,run,n_steps,n_agents,df_type='MF')
        Write2CSV(HF_out_file,HF_data_columns,dataframe,run,n_steps,n_agents,df_type='HF')

    elapsed_time = time.time() - start_time

    print("Profile "+str(profile_id)+" took "+str(elapsed_time)+" seconds.")

##########################################################################################################

### Initiate Multiprocessing

if __name__ == '__main__':

    # Start profiling time
    model_start_time = time.time()

    processes = []

    for profile_id in expt_data["run_profiles"]:
        p = multiprocessing.Process(target=run_profile, args=(expt_data,profile_id,))
        processes.append(p)
        p.start()
        
    for process in processes:
        process.join()

    # Profiling Ends and Delta reported
    model_elapsed_time = time.time() - model_start_time
    print("Experiment simulated in "+str(model_elapsed_time)+" seconds.")
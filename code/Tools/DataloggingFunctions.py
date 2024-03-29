
import numpy as np
import pandas as pd
import json

#%%

# DATALOGGING FUNCTIONS

# --------------------------
# CHANGE COUNT FUNCTION
# --------------------------
#
# DESCRIPTION: From a matrix of boolean states, it tracks the changes of state in time,
#              records when did these state changes happen, which cells (Agents) changed and
#              how many 'True' values were present after the change.
#              Used for logging the Idea, PV_alone and PV_community variables
#
# INPUT ARGUMENTS
#
# -bool_mat    -> boolean matrix under analysis
#
# OUTPUT ARGUMENTS
#
# -time_changes_list    -> List with all the timesteps in which there was a change in state
# -count_list           -> List with the count of 'True' values at each timestep in time_changes_list
# -changers_list        -> List with a list of the changing Agents at each timestep in time_changes_list

def ChangeCount(bool_mat):

    # Vector with the total number of 'True' values on each timestep = sum over Agent dimension
    count_v = bool_mat.sum(axis=1)

    # Matrix of changes per timestep -> XOR Operation with shifted input matrix
    change_mat = bool_mat[1:bool_mat.shape[0]]^bool_mat[0:bool_mat.shape[0]-1]
    change_mat = np.insert(change_mat,0,1,axis=0)   # Consider time 0 as everyone changing to initial state.

    # Vector with the total number of changes on each timestep
    count_change = change_mat.sum(axis=1)

    changers_list = []          # List that will contain the Agents that have changed
    count_list = []             # List that will contain the number of 'True' states after the change
    time_changes_list = []      # List with the timesteps of each change

    # Iterate over the change vector
    for i in range(0,count_change.size):

        # If there are any changes at timestep i
        if(count_change[i]>0):

            a_list = []

            # Iterate over the Agents of timestep i
            for j in range(0,change_mat.shape[1]):

                # If Agent j on timestep i has changed
                if(change_mat[i][j]):

                    a_list.append(j)        # Add Agent j to list of agents
            
            changers_list.append(a_list)    # Add list of agents to changers_list
            time_changes_list.append(i*2)   # Add time to list (x2 CORRECTION -> Each step is counted as 2 by collector)
            count_list.append(count_v[i])   # Add number of agents with 'True' to list

    return time_changes_list, count_list, changers_list

#%%

# --------------------------
# INITIALIZE CSV FUNCTION
# --------------------------
#
# DESCRIPTION: Creates (or resets, if existant) a CSV File and writes the column indexes.
#
# INPUT ARGUMENTS
#
# -filename   -> name of the csv file to create/initialize
# -columns    -> list of desired column indexes
#

def InitializeCSV (filename,columns,indexes):

    df = pd.DataFrame(columns=indexes)
    idx = pd.MultiIndex.from_frame(df)

    header = pd.DataFrame(columns=columns,index=idx)  # Create an empty dataframe with only the header with the column indexes

    header.to_csv(filename, sep=';', mode='w', header=True)     # Write the column indexes overwriting existing data

    return

#%%

# --------------------------
# WRITE TO CSV FUNCTION
# --------------------------
#
# DESCRIPTION: Writes logging data to a previously initialized csv file in one of the two dataframe types
#              used: either HF (High Frequency) DataFrame or MF (Medium Frequency) DataFrame. It does not
#              overwrite existing data, so it can be applied iteratively.
#
# INPUT ARGUMENTS
#
# -filename             -> name of the csv file to write to
# -columns              -> list of desired column indexes
# -collector_dataframe  -> complete dataframe from the model's data collector
# -run                  -> model run# in the context of a batch
# -n_steps              -> number of steps executed
# -n_agents             -> number of agents in the model
# -seed                 -> seed of current run
# -df_type              -> type of DataFrame (either ='MF' or ='HF', otherwise it will give an error)
#
# OUTPUT ARGUMENTS
#
# -err                  -> returns 1 if has detected an error
#

def Write2CSV (filename,columns,collector_dataframe,run,n_steps,n_agents,df_type='HF'):

    err=0   # If nothing bad happens, err remanins at 0

    # If we want to write a High Frequency DataFrame
    if df_type == "HF":
                
        collector_dataframe.insert(0,"Run",np.full(len(collector_dataframe.index),run)) # Insert Run column
        dataframe_truncated = collector_dataframe[columns]  # Truncate the complete dataframe only with the columns we want
        dataframe_truncated.to_csv(filename, sep=';', mode='a', header=False)   # Write data to CSV, without header and in append mode

    # If we want to write a Medium Frequency DataFrame
    elif df_type == "MF":
        
        # Create data Matrices from the input DataFrame in order to analyze them
        pv_alone_mat = np.reshape(collector_dataframe.pv_alone.to_numpy(),(n_steps,n_agents))
        pv_com_mat = np.reshape(collector_dataframe.pv_community.to_numpy(),(n_steps,n_agents))
        Com_Idea_mat = np.reshape(collector_dataframe.community.to_numpy(),(n_steps,n_agents))

        # Analyze the PV_alone Matrix with CHANGE COUNT Function to get the corresponding set of lists
        pv_alone_t, pv_alone_cnt, pv_alone_chg = ChangeCount(pv_alone_mat)

        # Create dataframe from obtained lists
        dataframe_pv_alone = pd.DataFrame(list(zip(pv_alone_cnt,pv_alone_chg)),index=pv_alone_t,columns=['PV_alone_cnt','PV_alone_chg'])
        dataframe_pv_alone.index.name = 'Step'

        # Analyze the PV_community Matrix with CHANGE COUNT Function to get the corresponding set of lists
        pv_com_t, pv_com_cnt, pv_com_chg = ChangeCount(pv_com_mat)

        # Create dataframe from obtained lists
        dataframe_pv_com = pd.DataFrame(list(zip(pv_com_cnt,pv_com_chg)),index=pv_com_t,columns=['PV_com_cnt','PV_com_chg'])
        dataframe_pv_com.index.name = 'Step'
        
        # Analyze the Idea Matrix with CHANGE COUNT Function to get the corresponding set of lists
        Com_Idea_t, Com_Idea_cnt, Com_Idea_chg = ChangeCount(Com_Idea_mat)

        # Create dataframe from obtained lists
        dataframe_com_idea = pd.DataFrame(list(zip(Com_Idea_cnt,Com_Idea_chg)),index=Com_Idea_t,columns=['Com_Idea_cnt','Com_Idea_chg'])
        dataframe_com_idea.index.name = 'Step'

        # Merge the dataframes with the join function. Values on one DataFrame that don't exist on the other are replaced by NaN
        joint_dataframe = dataframe_pv_alone.join(dataframe_pv_com,how='outer')
        joint_dataframe = joint_dataframe.join(dataframe_com_idea,how='outer')

        # Add current run to Run column
        joint_dataframe.insert(0,"Run",np.full(len(joint_dataframe.index),run))

        # Write to CSV
        joint_dataframe.to_csv(filename, sep=';', mode='a', header=False) # Write data to CSV, without header and in append mode

    # Erroneous Type
    else:
        err=1
        print("CSV ERROR: Type not recognized.")

    return(err)


#%%

# --------------------------
# READ CSV BATCH
# --------------------------
#
# DESCRIPTION: Reads a CSV batch, including input and output data and returns all useful variables.
#
# INPUT ARGUMENTS
#
# -curr_profile     -> number of batch to read
# -profile_suffix   -> string with the suffix used for data storage, eg "profile_"
#   
# OUTPUT ARGUMENTS
#
# -HF_data      -> High Frequency Dataframe
# -MF_data      -> Medium Frequency Dataframe
# -x_coord      -> Array with building x-coordinates
# -y_coord      -> Array with building y-coordinates
# -n_runs       -> Total number of runs
# -n_steps      -> Total number of steps
# -n_agents     -> Total number of agents
# -input_dict   -> Input data dictionary from profile
# -seeds        -> Array with seeds for all runs, in order
#
# HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds

def ReadCSVBatch (expt_name,curr_profile,profile_suffix):

    # Systematical naming for input and output files                                
    curr_profile_name = profile_suffix+str(curr_profile)     # Current Profile name
    m_prof_file = "Data/Experiments/" + expt_name + "/" + curr_profile_name + ".json"         # Current input profile
    m_data_file = "Data/buildings_meta.json"

    # Datalogging files
    HF_data_file = "Datalogs/Logs/" + expt_name + "/" + curr_profile_name + "_HF.csv"
    MF_data_file = "Datalogs/Logs/" + expt_name + "/" + curr_profile_name + "_MF.csv"
    Coord_file = "Datalogs/Logs/" + expt_name + "/" + curr_profile_name + "_Coordinates.csv"

    # Input JSON File
    with open(m_data_file) as myjson:
        input_dict = json.loads(myjson.read())

    with open(m_prof_file) as myjson:
        input_dict.update(json.loads(myjson.read()))

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

    return HF_data,MF_data,x_coord,y_coord,n_runs,n_steps,n_agents,input_dict,seeds

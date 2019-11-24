import numpy as np
import pandas as pd

#%%

# --------------------------
# AVERAGE HF DATAFRAME FUNCTION
# --------------------------
#
# DESCRIPTION: gets the average value of the HF data of a dataframe through its runs and
#              drops the 'Run' dimension
#
# INPUT ARGUMENTS
#
# -dataframe    -> HF Dataframe
# -n_runs       -> number of runs
# -n_steps      -> number of steps per run
# -n_agents     -> number of agents
#
# OUTPUT ARGUMENTS
#
# -avg_dataframe -> dataframe of average values
#

def AverageHFDataframe(dataframe,prev_average_dataframe,curr_run,n_runs,n_steps,n_agents):

    # Factor for averaging the data
    avg_factor = 1/n_runs

    # The first run for initialization
    if(curr_run==0):

        # Initialize the average as the first value and scale it with the avg_factor
        avg_dataframe = np.multiply(dataframe,avg_factor)
        
    else:

        # Avg data = Avg data + factor*curr_data
        Data_curr_run = np.multiply(dataframe,avg_factor)
        avg_dataframe = np.add(prev_average_dataframe,Data_curr_run)

    return avg_dataframe


#%%

# --------------------------
# COUNT VARS LIST FUNCTION
# --------------------------
#
# DESCRIPTION: from a MF Dataframe, it extracts the counting information
#              of a states variable in a way that is treatable by the
#              MultiLinePlot function
#
# INPUT ARGUMENTS
#
# -dataframe        -> MF Dataframe
# -col_to_analyze   -> String with the name of the column to analyze (only 1)
# -runs_to_analyze  -> number of runs to consider
# -n_steps          -> number of steps per run
#
# OUTPUT ARGUMENTS
#
# -Change_time_list -> list with one time array per each run, with the timesteps of changes
# -Count_list       -> list with one data array per each run, with the count value after the change
#

def CountVarsList(dataframe,col_to_analyze,runs_to_analyze,n_steps):

    # Init lists
    Change_time_list = []
    Count_list = []

    # For all the wanted runs
    for run in range(0,runs_to_analyze):

        # Take the data on that run
        Data_onrun = dataframe[dataframe.index.get_level_values('Run') == run].droplevel('Run')

        # Extract arrays: time and count values
        Change_t = Data_onrun[[col_to_analyze]].dropna().index.to_numpy()/2       # Correct scale factor - Collector counts 2 steps!
        Count = Data_onrun[[col_to_analyze]].dropna().to_numpy().transpose()
        Count = np.reshape(Count,np.size(Count))

        # Add last state - Otherwise step plot looks like garbage
        Change_t = np.append(Change_t,n_steps)
        Count = np.append(Count,Count[np.size(Count)-1])

        # Append run data arrays to the lists
        Change_time_list.append(Change_t)
        Count_list.append(Count)
    
    return Change_time_list, Count_list

#%%

# --------------------------------------
# RECONSTRUCT BOOLEAN MATRIX FUNCTION
# --------------------------------------
#
# DESCRIPTION: from a MF Dataframe, reconstructs the complete State Matrix for a
#              specific run of the model.
#
# INPUT ARGUMENTS
#
# -dataframe        -> MF Dataframe
# -countername      -> string with the name of the counter column
# -changelistname   -> string with the name of the change list column
# -run              -> run to analyze
# -n_steps          -> total number of steps
# -n_agents         -> total number of agents
#
# OUTPUT ARGUMENTS
#
# -Matrix           -> Matrix that contains the state values with dimensions: (n_steps, n_agents)
#

def ReconstructBoolMatrix(dataframe,countername,changelistname,run,n_steps,n_agents):

    # Extract the data corresponding to the required run, and drop the 'Run' index
    dataframe = dataframe[dataframe.index.get_level_values('Run') == run].droplevel('Run')

    # Extract the array of times of change
    Change_t = dataframe[[countername]].dropna().index.to_numpy()/2       # Correct scale factor - Collector counts 2 steps!
    
    # Extract the array of counts
    Counts = dataframe[[countername]].dropna().to_numpy().transpose()
    Counts = np.reshape(Counts,np.size(Counts))
    
    # Extract the array of change lists
    Changes = dataframe[[changelistname]].dropna().to_numpy().transpose()
    Changes = np.reshape(Changes,np.size(Changes))

    # Initialize the matris to zeros
    Matrix = np.zeros((n_steps,n_agents))

    # If there is any change at all (otherwise the matrix stays 0)
    if len(Change_t)>1:

        Change_list = []

        # Convert the lists of changes into integer values
        for j in range(0,len(Changes)):

            # Split the initial string into an array of strings wrto the commas
            Curr_vect = Changes[j][1:len(Changes[j])-1].split(',')

            #Convert the String values of the array into Integers and append the new array to the list
            Curr_vect = [int(i) for i in Curr_vect]
            Change_list.append(Curr_vect)

        # Iterate for all steps
        for step in range(0,n_steps):
                
                # For steps bigger than 0 (we suppose that all values are 0 at Step=0)
                if(step>0):

                    # Copy the values from the previous step
                    Matrix[step,:]=Matrix[step-1,:]

                    # If the current step is in the list of times of change
                    if(step in Change_t):

                        # Get the index of the current step
                        idx = np.where(Change_t == step)[0][0]

                        # Iterate over all changing agents
                        for pos in range(0,len(Change_list[idx])):

                            # Set agent state to True
                            Matrix[step,Change_list[idx][pos]]=True
    
    return Matrix
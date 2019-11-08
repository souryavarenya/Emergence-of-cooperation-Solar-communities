#%%
# Import packages from standard library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import packaches from mesa library

# Import main classes from mesa package
from mesa import Agent, Model

# Import random agent activator
from mesa.time import RandomActivation

# Import space package
from mesa.space import MultiGrid
#--> SingleGrid - uses a grid lattice that allows only one agent per cell
#--> MultiGrid - uses a grid lattice that allows multiple agents per cell

# Import data collector object class
from mesa.datacollection import DataCollector

#%%
# MODEL FUNCTIONING
# --> See ..._run.py for running the code


#%%
# Define main object classes in the code

###############################################################################
#######################       Model      ######################################
###############################################################################

class BuildingModel(Model):
    """A model with some number of agents."""
    
    def __init__(self):
        '''
        This method initializes the instantiation of the model class.
        Inputs:
            ?
            ?
        '''        
        # 0. Read in Building and Neighborhood Data
        # !!! Only 10 Buildings for faster debugging 
        buildings_data = pd.read_csv("../01_Data/buildings_data.csv",
                                     nrows = 10)
        
        min_x = min(buildings_data["building_coord_x"])
        min_y = min(buildings_data["building_coord_y"])
        
        buildings_data["xcoord"] = buildings_data["building_coord_x"] - min_x
        buildings_data["ycoord"] = buildings_data["building_coord_y"] - min_y
        
        buildings_n = len(buildings_data["xcoord"])
        
        # 1. Define the number of agents in the model
        self.num_agents = buildings_n
        
        # 2. Define the spatial dimension of the model creating a grid
        # Set grid width and height based on location of buildings
        neighborhood_width = int(round(max(buildings_data["xcoord"]))) + 1
        neighborhood_height = int(round(max(buildings_data["ycoord"]))) + 1
        # Create the grid with calculated dimensions
        self.grid = MultiGrid(neighborhood_width,
                              neighborhood_height,
                              False)
        # Note: "False" input means grid is not toroidal, this means that 
        # the edges of the grid do not wrap around.
        
        # 3. Define activator method used in the model
        self.schedule = RandomActivation(self)
        
        # 4. Define a variable for conditional shut off of the model
        self.running = True
        # Note: here set as always true so model runs until max step.
        
        # 5. Setup Global Variables
        self.profit = 0.5
        self.awareness = 0.5
        self.social = 0.5
        self.neighbor = 0.5
        self.threshold = 0
        
        self.profit_weight = 0.2
        self.awareness_weight = 0.2
        self.social_weight = 0.3
        self.neighbor_weight = 0.3
        
        self.threshold_low = 0.5
        self.threshold_high = 0.75
        
        # Create agents
        for i in range(self.num_agents):
            a = BuildingAgent(i, self)
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = int(round(buildings_data.at[i,"xcoord"]))
            y = int(round(buildings_data.at[i,"ycoord"]))
            
            print("new_agent")
            print(x)
            print(y)
            print(i)
            
            self.grid.place_agent(a, (x,y))
    
        self.datacollector = DataCollector(
            #model_reporters={"Gini": compute_gini},  
            #agent_reporters={"Wealth": "wealth"}
            )        
               
    def step(self):
        '''Advance the model by one step.'''
        #self.datacollector.collect(self)
        self.schedule.step()   


###############################################################################
#######################       Agent      ######################################
###############################################################################

class BuildingAgent(Agent):
    """
    Creates a building owner agent.
    """
    
    def __init__(self, unique_id, model):
        '''
        Initializes all the attributes of the building owner agent.
        '''
        # To do:
        # 1. Update agent attribute initialization
        # 1.1 set awareness based on normal distribution
        # 1.2 set profit based on payback period calculation
        # 1.3 set social pressure as result of relative agreement algorithm
        # 1.4 set neighbor effect as calculation of nearby adopters
        # 2. Create mechanism to form a social network for each agent during
        # the agent initialization
        # 3. Create process for updating the attributes that change over time
        # 3.1 profit -> via payback calculation
        # 3.2 social -> via relative agreement algorithm
        # 3.3 neighbor -> via fraction of nearby adopters
        # 4. Create process for joining community        
        
        # Set the agent's unique_id from the model object
        super().__init__(unique_id, model)
        
        # Set the agent's attributes
        # Currently, all agents take the same values defined for model
        
        # Define agent's payback period
        # ***to-do: update this to change every time step and depend on 
        # agent's attributes, solar and electricity prices***
        self.profit = model.awareness
        # Define the agent's environmental awareness
        # ***to-do: take value from normal distribution***
        self.awareness = model.awareness
        # Define initial social pressure
        # ***to-do: initialize to zero?***
        self.social = model.social
        # Define neighbor effect
        # ***to-do: initialize to zero?***
        # Q: does it need to be an attribute?
        self.neighbor = model.neighbor
        
        # Define the threshold for developing the intention:
        # (a) to adopt solar PV -> threshold_low
        self.threshold_low = model.threshold_low
        # (b) to adopt solar PV and join a solar community -> threshold_high
        self.threshold_high = model.threshold_high
        
        # Initialize the agent's attributes that track adoption process
        # By default, no agent has intention to adopt solar or alreay has it
        
        # Track if the agent develops the intention to adopt solar PV
        self.idea = False
        # Track if the agent develops the intention to join a solar community
        self.community = False
        # Track if the agent has adopted solar PV individually
        self.pv_alone = False
        # Track if the agent has joined a solar community
        self.pv_community = False
        
        
    def step(self):
        '''
        This method describes what the agent does when activated.
        '''
        
        # 0. Check if the agent is already in a solar community
        if self.pv_community == True:
            
            # If the agent is in a solar community, then go on to next agent
            return
        
        # If the agent is not in a solar community, go through adoption process
        else:

            # 1. Update influence of peer effects            
            self.update_neighbor()
            
            # 2. Update payback period
            # to do
            
            # 3. Update social norms pressure
            # to do
            
            # 4. Update agent's utility
            # to do
            
            # 5. check the agent's intention
            
            # 5.0 if the utility is below threshold for adoption
            if self.utility < self.threshold_low:
                
                # go on to next agent
                return
            
            # 5.1 if the utility is above threshold for adoption
            elif self.utility >= self.threshold_low:
                
                # Set adoption intention True
                self.idea = True
                
                # if agent does not have solar PV yet, install it
                if self.pv_alone == False:
                    self.adopt_individual()
                    
                # 5.2 if the utility is above threshold for community
                if self.utility >= self.threshold_high:
                    
                    # Set intention to join community True
                    self.community = True
                    
                    # Join community
                    self.join_community()           

    def get_idea(self):
        '''
        This method determines if the agent develops the intention of
        adopting solar PV or not, and joining a solar community or not.
        Input:
            None (based on values of agent attributes)
        Output:
            None (it modifies agent attributes self.idea and self.community).
        '''
        
        # 1. Compute the agent's utility
        self.utility = self.profit * self.model.profit_weight + self.awareness * self.model.awareness_weight
        
        # 2. Compare the agent's utility to the threshold for:
        # 2.a Developing the intention to install solar PV alone
        if self.utility > self.model.threshold_low:
            self.idea = True
        # 2.b Developing the intention to install solar & join a community
        if self.utility > self.model.threshold_high:
            self.community = True
            
        
    def adopt_individual(self):
        '''
        This method installs a solar PV system in the agent's rooftop.
        '''
        self.pv_alone = True
        
    def join_community(self):
        '''
        This method tries to integrate agent in a solar community.
        '''
        self.pv_community = True
                
                
    def update_neighbor(self):
        '''
        This method updates the peer effect of nearby adopters.
        '''
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        cellmates_community = 0
        for mates in cellmates:
                if mates.community == True:
                    cellmates_community += 1
        
        self.neighbor = cellmates_community / len(cellmates)
    

        

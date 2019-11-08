from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import pandas as pd

# MODEL FUNCTIONING
# --> See ..._run.py for running the code



#####################################################################################
#############################       Model      ######################################
#####################################################################################

class BuildingModel(Model):
    """A model with some number of agents."""
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.running = True
        
        # Read in Building and Neighborhood Data
        # !!! Only 10 Buildings for faster debugging 
        buildings_data = pd.read_csv("../01_Data/buildings_data.csv", nrows = 10)
        
        buildings_data["xcoord"] = buildings_data["building_coord_x"] - min(buildings_data["building_coord_x"])
        buildings_data["ycoord"] = buildings_data["building_coord_y"] - min(buildings_data["building_coord_y"])
        
        neighborhood_width = int(round(max(buildings_data["xcoord"]))) + 1
        neighborhood_height = int(round(max(buildings_data["ycoord"]))) + 1
        
        buildings_amount = len(buildings_data["xcoord"])
        
        self.num_agents = buildings_amount
        self.grid = MultiGrid(neighborhood_width, neighborhood_height, True)
        
        # Setup Global Variables
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
            #model_reporters={"Gini": compute_gini},  # `compute_gini` defined above
            #agent_reporters={"Wealth": "wealth"}
            )        
               
    def step(self):
        '''Advance the model by one step.'''
        #self.datacollector.collect(self)
        self.schedule.step()   


#####################################################################################
#############################       Agent      ######################################
#####################################################################################

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
        
        # Initialize the agent's attributes that track progress in adoption process
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
        #The agent's step will go here.
        self.update_neighbor()
        self.get_idea()
        self.adopt()
        
        

    def get_idea(self):
        self.utility = self.profit * self.model.profit_weight + self.awareness * self.model.awareness_weight
        
        if (self.utility > self.model.threshold_low) & (self.utility < self.model.threshold_high):
            self.idea = True
        
        if self.utility > self.model.threshold_high:
            self.community = True
            
        
    def adopt(self):
        # Check for PV alone adoption
        if self.idea == True & self.community == False:
            self.pv_alone = True
        
        # Check for adoption in community
        if self.idea == True & self.community == True:
            
            # all "neighboring agents", so far all agents on the same grid
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            
            # 
            for mates in cellmates:
                if mates.community == True:
                    mates.pv_community == True
                    self.pv_community == True
                
                
    def update_neighbor(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        cellmates_community = 0
        for mates in cellmates:
                if mates.community == True:
                    cellmates_community += 1
        
        self.neighbor = cellmates_community / len(cellmates)
    

        

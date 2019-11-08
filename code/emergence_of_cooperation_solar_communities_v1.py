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
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.profit = model.awareness
        self.awareness = model.awareness
        self.social = model.social
        self.neighbor = model.neighbor
        self.threshold_low = model.threshold_low
        self.threshold_high = model.threshold_high
        
        self.idea = False
        self.community = False
        
        self.pv_alone = False
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
    

        
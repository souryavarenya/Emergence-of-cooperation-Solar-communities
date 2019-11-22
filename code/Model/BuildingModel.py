# Import Model class from mesa as a parent class for the model
from mesa import Model

### Import our agent from /Agent/BuildingAgent.py - NOT NEEDED ANYMORE!

# Import NetworkX Library
import networkx as nx

# Import random agent activator
from mesa.time import RandomActivation

# Import space package
from mesa.space import MultiGrid, ContinuousSpace 
#--> SingleGrid - uses a grid lattice that allows only one agent per cell
#--> MultiGrid - uses a grid lattice that allows multiple agents per cell
#--> Continuous Space

# Import data collector object class
from mesa.datacollection import DataCollector

class BuildingModel(Model):
    """A model with some number of agents."""
    
    def __init__(self, agent, b_data, n_agents, data_dict):
        '''
        This method initializes the instantiation of the model class.
        Inputs:
            agent       > Agent Model taken as an input
            b_data      > csv file with data about buildings
            n_agents    > number of building owners populating the model
            data_dict   > meta data of the data file containing properties like min_x, max_x, range_x,...
        '''                
        # 1. Define the number of agents in the model
        self.num_agents = n_agents
        
        # 2. Define the spatial dimension of the model creating a grid
        # Create the grid with calculated dimensions
        ## self.grid = MultiGrid(width, height, False)
        self.space = ContinuousSpace(data_dict["max_x"], data_dict["max_y"], False, data_dict["min_x"], data_dict["min_y"])
        # Note: "False" input means grid is not toroidal, this means that 
        # the edges of the grid do not wrap around.
        # In continuous space, all min and max co-ords can be given.
        
        # 3. Define activator method used in the model
        self.schedule = RandomActivation(self)
        
        # 4. Define a variable for conditional shut off of the model
        self.running = True
        # Note: here set as always true so model runs until max step.
        
        # 5. Setup Global Variables
        self.profit = data_dict["profit"]
        self.awareness = data_dict["awareness"]
        self.awareness_var = data_dict["awareness_var"]
        self.awareness_unc = data_dict["awareness_unc"]
        self.social = data_dict["social"]
        self.neighbor = data_dict["neighbor"]
        
        self.profit_weight = data_dict["profit_weight"]
        self.awareness_weight = data_dict["awareness_weight"]
        self.social_weight = data_dict["social_weight"]
        self.neighbor_weight = data_dict["neighbor_weight"]
        
        self.threshold_low = data_dict["threshold_low"]
        self.threshold_high = data_dict["threshold_high"]

        self.start_price = data_dict["start_price"]
        self.learning_rate = data_dict["learning_rate"]
        self.price = self.start_price

        self.idea_phase = True
        # Flag for switching between
        
        # 6. Visualization variables
        self.x_coord = []
        self.y_coord = []
        self.agent_list = []

        # Solar Community blocks
        self.communities = []

        # Create Small World Network between agents (Done before agents)
        self.num_neighbors_wsg = data_dict["swn_k"]
        self.rewire_prob_wsg = data_dict["swn_p"]
        self.net = self.init_small_world()
        
        # Create agents
        for i in range(self.num_agents):
            
            a = agent(i, self)
            
            # Add agent to model schedule
            self.schedule.add(a)
            
            # Add the agent to its cell
            x = b_data.at[i,"building_coord_x"]
            y = b_data.at[i,"building_coord_y"]

            a.block = b_data.at[i, "building_block"]
            
            # Get data for visualization
            self.x_coord.append(x)
            self.y_coord.append(x)
            self.agent_list.append(a)
            
            print("new_agent")
            print(x)
            print(y)
            print(i)
            
            self.space.place_agent(a,(x,y))

        self.datacollector = DataCollector(
            #model_reporters={"Gini": compute_gini},  
            #agent_reporters={"Wealth": "wealth"}
            )        
               
    def step(self):
        '''Advance the model by one step.'''
        #self.datacollector.collect(self)
        self.idea_phase = True
        self.schedule.step()
        
        self.idea_phase = False
        self.schedule.step()

        self.update_global_pv_price()   
        print("==")

    
    def update_global_pv_price(self):
        '''Update global pv prices. Agents can then use this global pv price for their idea calculation'''
        self.price = self.price / (1 + self.learning_rate)     # WRONG formula so far; so far we assume that the cumulative capacity doubles every year

    def init_small_world(self):
        return nx.generators.random_graphs.watts_strogatz_graph(self.num_agents, self.num_neighbors_wsg, self.rewire_prob_wsg)
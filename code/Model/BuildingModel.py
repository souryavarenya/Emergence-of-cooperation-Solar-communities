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
            data_dict   > meta data of the data file containing properties
                        like min_x, max_x, range_x,...
        '''                
        # 1. Define the number of agents in the model
        self.num_agents = n_agents
        
        # 2. Define the spatial dimension of the model creating a grid
        # Create the grid with calculated dimensions
        ## self.grid = MultiGrid(width, height, False)
        self.space = ContinuousSpace(data_dict["max_x"],
                                     data_dict["max_y"],
                                     False,
                                     data_dict["min_x"],
                                     data_dict["min_y"])
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
        
        # Weights of decision-making variables
        self.profit_weight = data_dict["profit_weight"]
        self.awareness_weight = data_dict["awareness_weight"]
        self.social_weight = data_dict["social_weight"]
        self.neighbor_weight = data_dict["neighbor_weight"]
        
        # Thresholds for solar individual (low) and community (high) intentions
        self.threshold_low = data_dict["threshold_low"]
        self.threshold_high = data_dict["threshold_high"]
        
        ### Initialize economic parameters
        
        # Maximum payback period beyond which agents see no profitability
        # in the adoption of solar PV [years]
        self.max_pbp = 15
        # Source: please, see agent.update_profit method.
        # ***PLEASE, MOVE TO .JSON WITH VALUE 15
        
        # Price of solar PV system [CHF/kW]
        self.pv_price = 2000
        #self.pv_price = data_dict["pv_price_0"]
        # ***PLEASE, UPDATE NAME IN .JSON AND VALUE TO 2000
        
        # Price of electricity [CHF/kWh]
        self.el_price = 0.30
        #self.el_price = data_dict["el_price_0"]
        # ***PLEASE, MOVE TO .JSON WITH VALUE 0.30   
        
        # Change of solar PV system prices every year [as fraction of prior]
        self.pv_price_yoy = 0.05
        # ***PLEASE, MOVE TO .JSON WITH VALUE 0.05
        
        # Change of electricity prices every year [as fraction of prior]
        self.el_price_yoy = 0.01
        # ***PLEASE, MOVE TO .JSON WITH VALUE 0.01        

        self.idea_phase = True
        # Flag for switching between phase steps
        
        # 6. Visualization variables
        self.x_coord = []
        self.y_coord = []
        self.agent_list = []

        # Create Small World Network between agents (Done before agents)
        self.num_neighbors_wsg = data_dict["swn_k"]
        self.rewire_prob_wsg = data_dict["swn_p"]
        self.net = self.init_small_world()
        
        # Create agents
        for i in range(self.num_agents):
 
            # Retrieve agent's location from data
            x = b_data.at[i,"building_coord_x"]
            y = b_data.at[i,"building_coord_y"]
            
            # Retrieve agent's block from data
            block = b_data.at[i, "building_block"]
            
            # Retrieve agent's electricity demand from data
            el_demand = b_data.at[i, "demand_kwh"]
            
            # Retrieve agent's solar potential from data
            pv_potential = b_data.at[i, "max_pv_gen_kwh"]
            
            # Determine the size of the solar PV system
            # We use a typical rule of thumb in the industry: size of PV system 
            # makes annual solar generation equal to annual electricity demand
            
            # Determing scaling factor acc to relation el_demand, pv_potential
            if el_demand < pv_potential:
                
                # If solar potential is larger than annual demand,
                # scale solar PV system to annual electricity demand
                pv_sf = el_demand / pv_potential
                
            else:
                
                # If solar potential is smaller than annual demand, 
                # build the largest solar PV system possible
                pv_sf = 1
            
            # Create agent
            a = agent(i, self, block, el_demand, pv_potential, pv_sf)
            
            # Add agent to model schedule
            self.schedule.add(a)
            
            # Locate agent in the map
            self.space.place_agent(a,(x,y))
            
            # Get data for visualization
#            self.x_coord.append(x)
#            self.y_coord.append(x)
#            self.agent_list.append(a)
            
#            print("new_agent")
#            print(x)
#            print(y)
#            print(i)         

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

        self.update_global_prices()   
        print("==")

    
    def update_global_prices(self):
        '''
        This method updates the prices of solar PV and electricity use for the
        computation of the payback periods of the agents.
        '''
        
        # Update solar PV price
        self.pv_price = self.pv_price * (1 - self.pv_price_yoy)
        
        # Update electricity prices from list
        self.el_price = self.el_price * (1 - self.el_price_yoy)

    def init_small_world(self):
        '''
        This method creates a small world network for the agent.
        '''
        
        return nx.generators.random_graphs.watts_strogatz_graph(self.num_agents,
                                                                self.num_neighbors_wsg,
                                                                self.rewire_prob_wsg)
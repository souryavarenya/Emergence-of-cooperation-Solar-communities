# Import Model class from mesa as a parent class for the model
from mesa import Model

### Import our agent from /Agent/BuildingAgent.py - NOT NEEDED ANYMORE!

# Import NetworkX Library
import networkx as nx

# Import numpy
import numpy as np

# Import random agent activator
from mesa.time import RandomActivation

# Import space package
from mesa.space import MultiGrid, ContinuousSpace 

# Import data collector object class
from mesa.datacollection import DataCollector

class BuildingModel(Model):
    """A model with some number of agents."""
    
    def __init__(self, agent, b_data, n_agents, data_dict, seed=None):
        '''
        This method initializes the instantiation of the model class.
        Inputs:
            agent       > Agent Model taken as an input
            b_data      > csv file with data about buildings
            n_agents    > number of building owners populating the model
            data_dict   > meta data of the data file containing properties
                        like min_x, max_x, ...
        '''                
        # 1. Define the number of agents in the model
        self.num_agents = n_agents

        self.myseed = seed

        # Initialize a dictionary of community blocks (block has more than 2 buildings)
        self.community_idea_blocks = { block_id:{} for block_id in data_dict["comm_blocks"]}
        self.community_install_blocks = { block_id:{} for block_id in data_dict["comm_blocks"]}
        # - community idea blocks    -> Dictionary of dictionaries containing agent id and corresponding community value for developed ideas
        # - community install blocks -> Dictionary of dictionaries containing agent id and corresponding community value for installations

        self.space = ContinuousSpace(data_dict["max_x"],
                                     data_dict["max_y"],
                                     False,
                                     data_dict["min_x"],
                                     data_dict["min_y"])
        # Note: "False" input means grid is not toroidal, this means that 
        # the edges of the grid do not wrap around.
        # In continuous space, all min and max co-ords can be given.
        
        # Define activator method used in the model
        self.schedule = RandomActivation(self)
        
        # Define a variable for conditional shut off of the model
        self.running = True
        # Note: here set as always true so model runs until max step.
        
        # Setup Global Variables
        self.awareness = data_dict["awareness"]
        self.awareness_var = data_dict["awareness_var"]

        # Get Alpha and Beta for PERT
        # alpha and beta calculated as shown here: https://stats.stackexchange.com/questions/12232/calculating-the-parameters-of-a-beta-distribution-using-the-mean-and-variance

        self.alpha = (self.awareness**2)*(((1-self.awareness)/(self.awareness_var**2))-(1/self.awareness))
        self.beta = self.alpha*((1/self.awareness)-1)

        if((self.alpha<1)or((self.beta<1))):
            print("WARNING: degenerate Beta for Awareness! Maybe awareness variance is too large?")

        # Rel Agreement Gain
        self.ra_gain = data_dict["ra_gain"]
        
        # Weights of decision-making variables
        self.profit_weight = data_dict["profit_weight"]
        self.awareness_weight = data_dict["awareness_weight"]
        self.neighbor_weight = data_dict["neighbor_weight"]
        
        # Thresholds for solar individual (low) and community (high) intentions
        self.threshold_low = data_dict["threshold_low"]
        self.threshold_high = data_dict["threshold_high"]
        
        ### Initialize economic parameters
        
        # Maximum payback period beyond which agents see no profitability
        # in the adoption of solar PV [years]
        self.max_pbp = data_dict["max_pbp"]
        # Source: please, see agent.update_profit method.
        
        # Price of solar PV system [CHF/kW]
        self.pv_price = data_dict["pv_price"]
        
        # Price of electricity [CHF/kWh]
        self.el_price = data_dict["el_price"] 
        
        # Change of solar PV system prices every month [as fraction of prior]
        self.pv_price_mom = (1 + data_dict["pv_price_yoy"])**(1/12) - 1
        
        # Change of electricity prices every month [as fraction of prior]
        self.el_price_mom = (1 + data_dict["el_price_yoy"])**(1/12) - 1

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

        pos_extremists = data_dict["pos_extremists"]
        neg_extremists = data_dict["neg_extremists"]
        pos_ext_list, neg_ext_list = self.make_extremists(pos_extremists, neg_extremists)
        
        np.random.seed(self.myseed)

        # Create agents
        for i in range(self.num_agents):
 
            # Retrieve agent's location from data
            x = b_data.at[i,"building_coord_x"]
            y = b_data.at[i,"building_coord_y"]
            
            # Creating an X,Y list for _____
            self.x_coord.append(x)
            self.y_coord.append(y)

            # Retrieve agent's block ID
            block = b_data.at[i, "building_block"]

            # Add agent to the community block initialized with False
            # Only possible if the agent lives in a block - so just attempt blindly. 
            try:
                self.community_idea_blocks[block].update({i:False})
                self.community_install_blocks[block].update({i:False})
            except KeyError:
                pass    
            
            # Retrieve agent's electricity demand from data [kWh/year]
            el_demand = float(b_data.at[i, "demand_kwh"])
            
            # Retrieve agent's solar potential from data [kWh/year]
            pv_potential = float(b_data.at[i, "max_pv_gen_kwh"])
            
            # Retrieve agent's self-consumption [fraction of solar electricity
            # consumed on-site]
            pv_sc = float(b_data.at[i, "self_consumption"])
            
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
            a = agent(i, self, block, el_demand, pv_potential, pv_sf, pv_sc,
                    is_extremist = "pos" if i in pos_ext_list else ("neg" if i in neg_ext_list else None),
                    seed = self.myseed)
            
            # Add agent to model schedule
            self.schedule.add(a)
            
            # Locate agent in the map
            self.space.place_agent(a,(x,y))
            
            # Define collector data
            self.datacollector = DataCollector(
                model_reporters ={
                    "Awareness" : "awareness"},
                agent_reporters ={
                    "Utility" : "utility",
                    "Opinion" : "awareness",
                    "Uncertainty" : "awareness_unc",
                    "Neighbor":"neighbor",
                    "Profit":"profit",
                    "pv_alone" : "pv_alone",
                    "community" : "community",
                    "pv_community": "pv_community"}       
                )

        pass
               
    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)

        # Agents are randomly activated to develop the idea
        self.idea_phase = True
        self.schedule.step()
        
        #
        self.idea_phase = False
        self.schedule.step()

        # Effectively, one time step of the model 
        # = 1 MONTH
        # = 2 Agent steps - one idea and one 

        self.update_global_prices()   
        #print("==")

    def make_extremists(self, pos_extremists, neg_extremists):
        if pos_extremists + neg_extremists != 0:
            rlist = self.random.sample(range(self.num_agents), pos_extremists + neg_extremists)
            return rlist[:pos_extremists], rlist[pos_extremists:]
        else:
            return [],[]
        # Returns a list of positive and negative extremists resp

    
    def update_global_prices(self):
        '''
        This method updates the prices of solar PV and electricity use for the
        computation of the payback periods of the agents.
        '''
        
        # Update solar PV price
        self.pv_price = self.pv_price * (1 - self.pv_price_mom)
        
        # Update electricity prices from list
        self.el_price = self.el_price * (1 - self.el_price_mom)

    def init_small_world(self):
        '''
        This method creates a small world network for the agent.
        '''
        
        return nx.generators.random_graphs.watts_strogatz_graph(self.num_agents,
                                                                self.num_neighbors_wsg,
                                                                self.rewire_prob_wsg,
                                                                seed=self.myseed)

import random

import numpy as np
from mesa import Agent

from Tools import RelativeAgreement, SimplePayback
## The above only works because they're called from the main script
## Ignore the linting


class BuildingAgent(Agent):
    """
    Creates a building owner agent.
    """    
    def __init__(self, unique_id, model, block, el_demand, pv_potential, pv_sf, is_extremist = False):
        '''
        Initializes all the attributes of the building owner agent.
        Inputs:
            self : agent object
            model : model object
            block : string, building block unique identifier
            el_demand : integer, annual electricity demand [kWh]
            pv_sf : float, scaling factor of PV system size agent may buy [-]
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

        # Flag for marking first step
        self.first_step = True
        
        # Set the agent's attributes
        # Currently, all agents take the same values defined for model
        self.block = block

        # Defining a list of contacts for the given agent from a given network
        self.connection_list = [n for n in model.net.neighbors(unique_id)]
        
        # Initialize agent's profitability
        # Agent's payback period pbp and profit set to zero
        # These parameters are recalculated every step
        self.pv_sf = pv_sf
        self.pbp = 0
        self.profit = 0
        
        # Define agent's solar generation potential
        self.pv_potential = pv_potential
        
        # Define agent's building block
        self.block = block

        # Define the agent's environmental awareness
        # Initializes a random value around the given mean awareness 
        # and clips it between 0 and 1
        # ***IMPORTANT RANDOM MANAGEMENT -> maybe we need to use the mesa
        # package random package instead of the numpy??
        if is_extremist == None:
            self.awareness = np.random.beta(model.alpha, model.beta)
            self.awareness_unc = 0.02 + self.awareness*(1 - self.awareness)
        elif is_extremist == "pos":
            self.awareness = 0.94
            self.awareness_unc = 0.03
        elif is_extremist == "neg":
            self.awareness = 0.06
            self.awareness_unc = 0.03

        # Define neighbor effect
        # ***to-do: initialize to zero?***
        # Q: does it need to be an attribute?
        self.neighbor = 0
        self.total_neighbors = 0

        # Define agent's utility level
        # By default, all agents start at zero
        self.utility = 0
        
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

        # Divide the step into idea formation and implementation
        # Flag for checking idea phase 
        
    def step(self):
        '''
        This method describes what the agent does when activated.
        '''
        # 0. Presets some variables that only need to be called once but
        # can't be initialized through __init__ because other agents haven't 
        # been created yet
        if self.first_step:
            self.set_fixed_vars()
            self.first_step = False

        # 0. Update parameters for all agents
        # (must happen only once in a model time step)
        if self.model.idea_phase == True:
            self.update_profit()
            self.update_awareness()
            self.update_neighbors()
            # ^ to be only done if there are more block neighbors
        
        # 0. Check if the agent is already in a solar community and if so, can move on to next agent
        if self.pv_community == True:
            pass
        
        # If the agent is not in a solar community, go through adoption process
        else:  
            if self.model.idea_phase == True:
                self.get_idea()
            else:
                self.implement_pv()   

    def set_fixed_vars(self):
        '''
        Function that sets the variables dependent on other agents after the
        creation of all agents
        '''
        # Counts the number of block neighbors a building has 
        if self.block in self.model.community_blocks:
            self.total_neighbors = len(self.model.community_blocks[self.block])-1
        else:
            self.total_neighbors = 0         
            
    def update_profit(self):
        '''
        Update profit of agent for idea calculation. 
        Model updates global PV prices
        
        This method is based on a simplified, linear relation of the results
        for stated willingness to adopt solar PV photovoltaics for
        different payback periods by households in the U.S. as reported in:
        Conference paper Figure 3 in Sigrin and Drury (2014)
        https://pdfs.semanticscholar.org/4ea3/669e1d2058dc01bfd0baf5e0532ed3a6dbf6.pdf
        Full paper (w/o referenced figure): Sigrin, Pless, Drury (2015)
        https://doi.org/10.1088/1748-9326/10/8/084001      
        '''
        # Compute payback period with current prices
        self.pbp = SimplePayback.compute_pbp(self, 
                                             self.pv_sf, 
                                             self.pv_potential)
        
        # Estimate profitability perception of agent
        self.profit = 1 - (self.pbp / self.model.max_pbp)

    def update_awareness(self):
        '''
        This method models the social interactions of the agent with 
        other agents in its social network, and how both agents' awareness
        and uncertainty are modified as a result of the interaction.
        '''
        
        # Selects a connection randomly
        sel_connection = random.choice(self.connection_list)

        # initial opinion and uncertainty values of self
        opunc0 = (self.awareness,self.awareness_unc)

        # initial pinion and uncertainty values of selected connection
        connection_agent = self.model.schedule._agents[sel_connection]
        opunc1 = (connection_agent.awareness,connection_agent.awareness_unc)

        # Update the opuncs
        opunc0, opunc1 = RelativeAgreement.interact(opunc0, opunc1, self.model.ra_gain)

        # Assign new opunc values to self
        self.awareness = opunc0[0]
        self.awareness_unc = opunc0[1]

        # Assign new opun values to connection
        connection_agent.awareness = opunc1[0]
        connection_agent.awareness_unc = opunc1[1]

    def update_neighbors(self):
        '''
        Update neighbor parameter for idea calculation. Agent calculates 
        the share of buildings in their building block having a pv adopted
        '''
        if self.total_neighbors != 0:
            self.neighbor = sum(self.model.community_blocks[self.block].values())/self.total_neighbors

    def get_idea(self):
        '''
        This method determines if the agent develops the intention of
        adopting solar PV or not, and joining a solar community or not.
        Input:
            None (based on values of agent attributes)
        Output:
            None (it modifies agent attributes self.idea and self.community).
        '''      
        # 5. check the agent's intention
        # Factor payback period
        f_pp = self.profit * self.model.profit_weight
        # Factor awareness
        f_aw = self.awareness * self.model.awareness_weight
        # Factor peer effects
        f_pe = self.neighbor * self.model.neighbor_weight
        # Update agent's utility
        self.utility = min([f_pp + f_aw + f_pe, 1])
        
        # print("\n--\nHi there, I am agent " + str(self.unique_id) +
        #       " and I have a utility level of " + str(round(self.utility,2)) + 
        #       " during the step number " + str(self.model.schedule.steps) +
        #       ".")
        
        # 5. Compare the agent's utility to the threshold for:
        # 5.a Developing the intention to install solar PV alone
        if self.utility >= self.model.threshold_low:
            self.idea = True
        # 5.b Developing the intention to install solar & join a community
        if self.utility >= self.model.threshold_high:
            self.community = True

    def implement_pv(self):
        '''
        This method is for the agent to implement his idea into either individual 
        or community solar PV
        '''
        # Check if the agent develop the intention
        if self.idea == True:
            
            # If the agent developped the intention to join a community
            if self.community == True:
                self.join_community()
            
            # If the agent didn't develop the intention to join a community
            # and does not yet have solar on its rooftop
            elif self.pv_alone == False:
                self.adopt_individual()
                
            else:
                # If the agent didn't want to join a community and already
                # has solar in its rooftop, go on to next agent
                pass
        else:
            
            # If the agent did not develop the intention
            pass
            
    def adopt_individual(self):
        '''
        This method installs a solar PV system in the agent's rooftop.
        '''
        self.pv_alone = True
        
        # print("\nOh wow! I just install solar PV on my rooftop!" +
        #       "\nMy id is " + str(self.unique_id) + 
        #       ", and my utility is " + str(self.utility) +
        #       ".")
        
    def join_community(self):
        '''
        This method integrates the agent in a solar community.
        '''
        self.pv_alone = True
        
        try:
            self.model.community_blocks[self.block].update({self.unique_id:True})
            self.pv_community = True
        except:
            pass
        
        # print("\nSweet! Just joined a community!" +
        #       "\nMy id is " + str(self.unique_id) + 
        #       ", and my utility is " + str(self.utility) +
        #       ".")

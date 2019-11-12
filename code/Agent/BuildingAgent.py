from mesa import Agent

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
        self.awareness = self.random.triangular(0,1, 0.5)
        # Define initial social pressure
        # ***to-do: initialize to zero?***
        self.social = model.social
        # Define neighbor effect
        # ***to-do: initialize to zero?***
        # Q: does it need to be an attribute?
        self.neighbor = model.neighbor
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
        
    def step(self, idea_phase):
        '''
        This method describes what the agent does when activated.
        '''

        # 0. Update parameters for all agents
        self.update_profit()
        self.update_awareness()
        self.update_neighbors()
        self.update_social()

        
        # 0. Check if the agent is already in a solar community
        if self.pv_community == True:
            
            # If the agent is in a solar community, then go on to next agent
            pass
        
        # If the agent is not in a solar community, go through adoption process
        else:
            
            # Agents need to update values here, in get_idea or somewhere else
            # TEST FUNCTION
            # profit increases 0.1 per time step
            self.profit += 0.1 * self.model.schedule.steps
            
            if idea_phase is True:
                self.get_idea()
            else:
                self.implement_pv()

            
            
    def update_profit(self):
        ''' Update profit of agent for idea calculation. Model updates global PV prices'''
        profit = 1 - self.model.price

    def update_awareness(self):
        pass

    def update_neighbors(self):
        ''' Update neighbor parameter for idea calculation. Agent calculates the share of buildings in their building block having a pv adopted'''
        pass

    def update_social(self):
        pass


    def get_idea(self):
        '''
        This method determines if the agent develops the intention of
        adopting solar PV or not, and joining a solar community or not.
        Input:
            None (based on values of agent attributes)
        Output:
            None (it modifies agent attributes self.idea and self.community).
        '''
        # 1. Update influence of peer effects            
        # self.update_neighbor()
        
        # 2. Update payback period
        # to do
        
        # 3. Update social norms pressure
        # to do
        
        # 4. Update agent's utility
        # to do
        
        # 5. check the agent's intention
        # Factor payback period
        f_pp = self.profit * self.model.profit_weight
        # Factor awareness
        f_aw = self.awareness * self.model.awareness_weight
        # Factor social pressure
        f_sp = self.social * self.model.social_weight
        # Factor peer effects
        f_pe = self.neighbor * self.model.neighbor_weight
        # Update agent's utility
        self.utility = min([f_pp + f_aw + f_sp + f_pe, 1])
        
        print("\n--\nHi there, I am agent " + str(self.unique_id) +
              " and I have a utility level of " + str(round(self.utility,2)) + 
              " during the step number " + str(self.model.schedule.steps) +
              ".")
        
        # 5. Compare the agent's utility to the threshold for:
        # 5.a Developing the intention to install solar PV alone
        if self.utility >= self.model.threshold_low:
            self.idea = True
        # 5.b Developing the intention to install solar & join a community
        if self.utility >= self.model.threshold_high:
            self.idea = True
            self.community = True

    def implement_pv(self):
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
        
        print("\nOh wow! I just install solar PV on my rooftop!" +
              "\nMy id is " + str(self.unique_id) + 
              ", and my utility is " + str(self.utility) +
              ".")
        
    def join_community(self):
        '''
        This method tries to integrate agent in a solar community.
        '''
        self.pv_alone = True
        self.pv_community = True
        
        print("\nSweet! Just joined a community!" +
              "\nMy id is " + str(self.unique_id) + 
              ", and my utility is " + str(self.utility) +
              ".")
        
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
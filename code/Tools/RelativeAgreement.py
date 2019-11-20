### Relative Agreement interaction - Takes in two opinion-uncertainty <tuples> 
# and returns respective modified op-unc return tuples
# opunc is in the range ([0,100],[0,50])
# reference http://jasss.soc.surrey.ac.uk/5/4/1.html

def interact(opunc0, opunc1, gain):
    '''
    This method modifies the opinion and uncertainty around that opinion of
    two agents that interact within a social network.
    Inputs:
        opunc0 : tuple, opinion value and uncertainty of agent 0
        opnuc1 : tuple, opinion value and uncertainty of agent 1
        gain : integer, controls speed of opinion dynamic
    Outputs:
        opunc0_mod : tuple, modified opinion value, uncertainty of agent 0
        opunc1_mod : tuple, modified opinion value, uncertainty of agent 1
    
    This formulation follows Deffuant et al (2002).
    http://jasss.soc.surrey.ac.uk/5/4/1.html
    '''
    # Expressed in the formulation employed by Deffuant et al (2002)
    # For agents i and j, their opinion is represented by x_i, x_j and
    # their uncertainty around that opinion by u_i, u_j.
    # In our tuples: opunc0 = (x_i, u_i), opunc1 = (x_j, u_j)
    
    # Measure the overlap of opinions between two agents
    # This follows Eq. 1 in Deffuant et al. (2002)
    # h_ij = min(x_i + u_i, x_j + u_j) - max(x_i - u_i, x_j - u_j)
    # In words, we measure the longest distance between the highest opinion
    # including uncertainty and the lowest opinion including uncertainty
    overlap = (min(opunc0[0]+opunc0[1],opunc1[0]+opunc1[1]) -
               max(opunc0[0]-opunc0[1],opunc1[0]-opunc1[1]))
    
    # Estimation of relative agreement for each agent
    # This follows Eq. 4 and 5 in Deffuant et al (2002)
    # RA(i,j)_i = gain * (h_ij/u_j - 1)
    # RA(i,j)_j = gain * (h_ij/u_i - 1)
    beta0 = gain*max(0,overlap/opunc1[1] - 1)
    beta1 = gain*max(0,overlap/opunc0[1] - 1)
    
    # Modified opinion value, uncertainty of agents
    # This follows Eq. 5 and 6 in Deffuant et al (2002)
    # For x_i, u_i being opinion and uncertainty of agent i
    # x_i_mod = x_i + RA(i,j) * (x_i - x_j)
    # u_i_mod = u_i + RA(i,j) * (u_i - u_j)
    opunc0_mod = tuple(map(lambda x0,x1:x0 + beta0*(x1 - x0),opunc0,opunc1))
    opunc1_mod = tuple(map(lambda x0,x1:x0 + beta1*(x1 - x0),opunc1,opunc0))
    
    # Return modified opinion value, uncertainty tuples
    return opunc0_mod, opunc1_mod


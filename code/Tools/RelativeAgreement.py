### Relative Agreement interaction - Takes in two opinion-uncertainty <tuples> and returns respective modified op-unc return tuples
# opunc is in the range ([0,100],[0,50])
# reference http://jasss.soc.surrey.ac.uk/5/4/1.html

def interact(opunc0, opunc1, gain):
    overlap = min(opunc0[0]+opunc0[1],opunc1[0]+opunc1[1]) - max(opunc0[0]-opunc0[1],opunc1[0]-opunc1[1])
    beta0 = gain*max(0,overlap/opunc1[1] - 1)
    beta1 = gain*max(0,overlap/opunc0[1] - 1)
    opunc0_mod = tuple(map(lambda x0,x1:x0 + beta0*(x1 - x0),opunc0,opunc1))
    opunc1_mod = tuple(map(lambda x0,x1:x0 + beta1*(x1 - x0),opunc1,opunc0))
    return opunc0_mod, opunc1_mod


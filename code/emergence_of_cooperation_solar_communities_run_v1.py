#%%
from emergence_of_cooperation_solar_communities_v1 import BuildingModel
import matplotlib.pyplot as plt
import numpy as np


#%%

### RUN MODEL

model = BuildingModel()

for i in range(2):
    model.step()
    
    
#agent_wealth = [a.wealth for a in model.schedule.agents]
#plt.hist(agent_wealth)

#%%
    
### BEHAVIORAL SPACE
    
    
#all_wealth = []
#for j in range(100):
#    # Run the model
#    model = MoneyModel(10)
#    for i in range(10):
#        model.step()
#        
#    for agent in model.schedule.agents:
#        all_wealth.append(agent.wealth)
#
#plt.hist(all_wealth, bins=range(max(all_wealth)+1))
    
#%%
    
### DATA VISUALIZATION OF GRID
  

agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()

#%%

### Get data from the DataCollector 

# for 1 measurement per step
gini = model.datacollector.get_model_vars_dataframe()
gini.plot()

# for multiple agents
agent_wealth = model.datacollector.get_agent_vars_dataframe()
agent_wealth.head()

end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
end_wealth.hist(bins=range(agent_wealth.Wealth.max()+1))

# for one agent out of out entire class
one_agent_wealth = agent_wealth.xs(14, level="AgentID")
one_agent_wealth.Wealth.plot()

#%%

### BATCH RUNNER
from mesa.batchrunner import BatchRunner

fixed_params = {
    "width": 10,
    "height": 10
}

variable_params = {"N": range(10, 500, 10)}

# The variables parameters will be invoke along with the fixed parameters 
# allowing for either or both to be honored.
batch_run = BatchRunner(
    MoneyModel,
    variable_params,
    fixed_params,
    iterations=5,
    max_steps=100,
    model_reporters={"Gini": compute_gini}
)

batch_run.run_all()

#%% 

### COLLECT BATCH DATA

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)













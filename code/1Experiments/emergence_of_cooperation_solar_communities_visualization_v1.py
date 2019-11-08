from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from emergence_of_cooperation_solar_communities_v1 import BuildingModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal


grid = CanvasGrid(agent_portrayal, 200, 200, 1000, 100)

#%%

server = ModularServer(BuildingModel,
                       [grid],
                       "Building Model"
                       )

#%%

server.port = 8525 # The default

#%%
server.launch()
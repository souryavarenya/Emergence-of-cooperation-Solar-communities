# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:55:24 2019

@author: anunezji
"""
#%%
# Import packages to handle data
import geopandas as gdp
import pandas as pd

#%%
# Set route to data files
route = r"C:\\Users\\anunezji\\Documents\\"

# Define files to be imported from route folder

# Files with geographical data
#file = "zone.shp"
file = "zone.shp"

# File with data about zones/blocks
data = "zones_data.csv"

# Import data files and store them in geopandas and pandas dataframes
shapefile = gdp.read_file(route+file)
data = pd.read_csv(route+data)

# Combine geographical and block data in a single dataframe
data_df = shapefile.set_index("Name").join(data.set_index("building_block"))

#%%
# Plot data

# Plot polygons, color code = max pv generation possible in block
#data_df.plot(column="max_pv_gen_kwh",
#             cmap="inferno",
#             figsize=(20,20))

# Plot polygons, color code = number of individual buildings per block
#data_df.plot(column="n_buildings",
#             cmap="Greens",
#             figsize=(20,20))

# Plot polygons, color code = existing solar capacity per block
data_df.plot(column="existing_pv_size_kw",
             cmap="Reds",
             figsize=(20,20))

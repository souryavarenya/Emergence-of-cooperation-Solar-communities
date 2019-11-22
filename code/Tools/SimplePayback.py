# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 12:48:13 2019

@author: anunezji
"""

def compute_pbp(self, pv_sf, pv_potential):
    '''
    This mehtod calculates the payback period of an individual solar PV
    installation for the agent.
    Inputs:
        self : agent
        pv_potential : integer, annual max solar generation [kWh]
        pv_sf : float, scaling factor of solar PV system size [-]
    Outputs:
        pbp : integer, number of years to recoup investment
        
    Note: this method is based on the simple payback period calculation for
    an investment. It has the following simplifactions and assumptions:
        1. Cashflows are assumed to stay constant over the years
        2. Investment cost is paid upfront
    '''
    #==========================================================================
    ### Data simplifications and assumptions
    # For simplicity and data availability reasons, we use the following values
    # for all agents:
    
    # Self-consumption, fraction of solar generation consumed on-site
    sc = 0.30
    # Average household self-consumes between 20-40% of solar PV generation
    # Source: Fraunhofer ISE (2019) Recent facts about photovoltaics in Germany
    
    # Operation and maintenance cost of solar PV system, as fraction 
    # of investment cost
    om = 0.015
    # Source: Peters et al (2011)
    # https://doi.org/10.1016/j.enpol.2011.07.045
    
    # Solar photovoltaic yield in Switzerland in kWh per kW
    sy = 975
    # @ALEJANDRO: ADD SOURCE
    
    # Remuneration for solar electricity fed to the grid in CHF/kWh
    pv_fg = 0.08
    # Source: EWZ 2016-2020 tariff
    # www.ewz.ch/webportal/de/privatkunden/
    # solaranlagen/solarstrom-fuer-eigentuemer/solaranlage.html
        
    # Assumptions:
    # 1. Agents size solar PV systems to meet annual demand or to maximum
    # rooftop area available
    # 2. Solar electricity generation is direclty proportional to system size
    # 3. Solar PV system price independent of system size
    #==========================================================================
    
    # Compute the size of the solar PV system in kW
    pv_size = pv_sf * pv_potential / sy    
    
    ### Determine the invesment cost in CHF
    pv_inv = pv_size * self.model.pv_price
    
    ### Determine annual cashflows
    
    # Avoided costs from reduced consumption of electricity from the grid CHF
    cf_ac = self.model.el_price * (sc * pv_sf * pv_potential)
    
    # Remuneration for solar electricity fed to grid CHF
    cf_fg = pv_sf * pv_potential * (1 - sc) * pv_fg
    
    # Operation and maintenance annual cost in CHF
    cf_om = - om * pv_inv
    
    # Annual cashflow of the project in CHF
    cf_pv = cf_ac + cf_fg + cf_om
    
    ### Determine number of years required to payback investment
    
    if cf_pv > 0:
        
        # If cashflows are positive, the number of years to pay back is given:
        pbp = pv_inv / cf_pv
    else:
        
        # If annual cashflows are negative, the agent will never be able to
        # recoup the investment costs
        pbp = self.model.max_pbp 

    # Condition the return before exiting
    pbp = min(int(round(pbp,0)), self.model.max_pbp)
    
    return pbp

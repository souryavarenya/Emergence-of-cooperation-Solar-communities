# Agent-Based Modeling and Social System Simulation 2019

> * Group Name: Red Panda
> * Group participants names: 
>   * Fornt Mas, Jordi
>   * Kovvali, Sourya
>   * Nuñez-Jimenez, Alejandro
>   * Schwarz, Marius
> * Project Title: Emergence of Co-operation for Solar Communities



## General Introduction

The diffusion of solar photovoltaic (PV) systems has the potential to decarbonize a large portion of the energy consumption in cities. However, consumers’ lack of awareness and uncertainty about solar PV hinder the diffusion the technology.

Opinion dynamics around the technology are thus of pivotal importance for understanding how policy interventions could accelerate the uptake of the technology.

Previous research points to the disproportionate influence of individuals with strong opinions – so-called “opinion extremists” – on other individuals within their social network. Such opinion extremists, therefore, provide a potential lever for policy interventions.

To investigate this influence, we have developped an agent-based model that represents a fraction of the building owners in Alt-Wiedikon district in Zurich, Switzerland. We simulate four scenarios with different distributions of opinion extremists to analyze their impact on the uptake of individual and community solar PV.

## The Model

The ABM represents the decision-making of building owners on whether to adopt rooftop solar individually or join a solar community based on economic and social factors.

The decision-making process has two steps, inspired by the theory of planned behavior (Ajzen 1991), where agents first determine if they develop the intention of adopting solar individually, of joining a community, or neither, and then implement the behavior (i.e., adopt individually or try to join a community).

The two most important variables to study with this model are the number of agents that install rooftop solar and the number of agents that join a solar community. Other intermediate variables such as the opinion quantification of the agents are also considered to gain a better understanding of the situation.

## Fundamental Questions

1. How does the presence of opinion extremists affect the adoption of solar installations and solar communities?
   
    1.1. How does the number of agents that adopt individual solar installations change with the insertion of opinion extremists?
   
    1.2. How does the number of agents that form solar communities change with the insertion of opinion extremists?

2. How does the presence of opinion extremists affect the opinion dynamics of the agent network?
   
    2.1. How does the average opinion of the agent network change with the insertion of opinion extremists?
   
    2.2. How do the opinion evolution functions of different agents change with the insertion of opinion extremists?

## Expected Results

1. Positive opinion extremists should stimulate the adoption of solar installations and communities, whereas negative opinion extremists should drag it down. Therefore:
   
    1.1. The number of solar installations should increase/decrease (respectively) with the insertion of positive/negative extremists.
   
    1.2. The number of solar communities should increase/decrease (respectively) with the insertion of positive/negative extremists.

2. The opinion dynamics of the agent network should shift towards the opinon values of the inserted extremists.
   
    2.1. The average opinion should increase/decrease (respectively) with the insertion of positive/negative extremists.
   
    2.1. The evolution functions of the agents should reflect a polarization of opinions around the extremists.

## References

Deffuant, G., Amblard, F., Weisbuch, G., & Faure, T. (2002). How can extremism prevail? A study based on the relative agreement interaction model. *Journal of artificial societies and social simulation*, *5*(4).

Schiera, D. S., Minuto, F. D., Bottaccioli, L., Borchiellini, R., & Lanzini, A. (2019). Analysis of rooftop photovoltaics diffusion in energy community buildings by a novel Gis-and agent-based modeling co-simulation platform. *IEEE Access*, *7*, 93404-93432.

Mehta, P., Griego, D., Nunez-Jimenez, A., & Schlueter, A. (2019, November). The Impact of self-consumption regulation on individual and community solar PV adoption in Switzerland: an agent-based model. In *Journal of Physics: Conference Series* (Vol. 1343, No. 1, p. 012143). IOP Publishing.

Other references in the document

## Research Methods

Agent-Based Model, Network Theory, Relative Agreement Interactions.

## Other

We are using a dataset kindly made available by Prakhar Mehta and Danielle Griego (see Mehta et al 2019), with data about buildings in the Alt-Wiedikon district of the city of Zurich. This includes geographical data about the location of buildings and the building blocks to which they belong, as well as data about the buildings’ annual electricity demand and potential solar generation.

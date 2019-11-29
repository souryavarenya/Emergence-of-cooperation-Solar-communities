# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import numpy as np
import math

#%%

# MATPLOTLIB-BASED VISUALIZATION FUNCTIONS

#%%

# --------------------------
# HISTOGRAM PLOT FUNCTION
# --------------------------
#
# DESCRIPTION: it creates a histogram plot from data.
#
# INPUT ARGUMENTS
#
# -data        -> vector with the data values to plot
# -n_bins      -> number of histogram categories
#
# -show        -> 1 if the image must be shown in screen
# -x_label     -> label that will appear on the x-axis
# -y_label     -> label that will appear on the y-axis
#
# -title       -> Title that will appear on the graph
# -size        -> Size of the graph (x,y)
# -cmap        -> Color map being used for the categories
# -save        -> 1 if the image must be saved into a .svg file
# -filename    -> Name that will be given to the image file
#

def HistogramPlot(data, n_bins=20, show=1, x_label="X_label", x_ax_lim = [], y_label="Y_label", cmap='RdYlGn', title="Title", size=(15,10), save=0, filename="test.svg"):

    #Configure Plot
    plt.figure(figsize=size)
    plt.title(title, fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)

    if(len(x_ax_lim)==2):
        plt.xlim(x_ax_lim)

    #Create Histogram
    a,b,patches = plt.hist(data,bins=n_bins)

    #Get color scheme
    viridis = cm.get_cmap(cmap, len(patches))

    #Color patches
    for i in range(0,len(patches)):
        color = viridis(i)
        thispatch = patches[i]
        thispatch.set_facecolor(color)

    #Save image if requested
    if(save==1):
        plt.savefig(filename, format='svg')

    #Show image if requested
    if(show==1):
        plt.show()


#%%

# --------------------------
# MULTI LINE PLOT FUNCTION
# --------------------------
#
# DESCRIPTION: it creates a plot with multiple lines or steps from an array of data.
#              Can be used to represent evolution of all agents, or evolution through all runs, etc
#
# INPUT ARGUMENTS
#
# -data        -> vector with the data values to plot
# -n_lines     -> number of lines to plot
#
# -x_axis      -> vector with x-coordinates (optional)
# -stepshape   -> 1 for Step Plot, 0 for Line Plot
#
# -show        -> 1 if the image must be shown in screen
#
# -subplot     -> 1 if used as a subplot
# -ax          -> If subplot==1, ax corresponding to the subplot
#
# -x_label     -> label that will appear on the x-axis
# -x_ax_lim    -> list with the limit values of the x-axis (min,max)
# -y_label     -> label that will appear on the y-axis
# -y_ax_lim    -> list with the limit values of the y-axis (min,max)
#
# -legend      -> 1 if a legend is wanted
# -legendlabel -> label to name the elements of the legend sequentially
#
# -title       -> Title that will appear on the graph
# -size        -> Size of the graph (x,y)
# -cmap        -> Color map being used to differentiate lines
# -save        -> 1 if the image must be saved into a .svg file
# -filename    -> Name that will be given to the image file
#

def MultiLinePlot(data, n_lines, x_axis=[], stepshape=0, show=1, subplot=0, ax= 0, x_label="X_label", x_ax_lim = [], y_label="Y_label", y_ax_lim = [], legend=1, legendlabel='Agent', cmap='RdYlGn', alpha=0.5, title="Title", size=(15,10), save=0, filename="test.svg"):

    #Configure Plot (only if it's not a subplot)
    if(subplot==0):
        plt.figure(figsize=size)
        plt.title(title, fontsize=16)
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)

        if(len(x_ax_lim)==2):
            plt.xlim(x_ax_lim)

        if(len(y_ax_lim)==2):
            plt.ylim(y_ax_lim)

    #Get color scheme for legend
    viridis = cm.get_cmap(cmap, n_lines)
    legend_elements = []

    #For every line to plot
    for i in range(0,n_lines):

        #If the input data is a List:
        if (type(data)==type([])):

            y_array = data[i]

            #If both x and y axes are inputs
            if(np.size(x_axis)==np.size(data)):
                x_array = x_axis[i]

            #Otherwise generate linear x axis
            else:
                x_array = range(0,len(data[:,i]))

        #Otherwise we assume it is a Matrix:
        else:

            y_array = data[:,i]

            #If both x and y axes are inputs
            if(np.size(x_axis)==np.size(data)):
                x_array = x_axis[:,i]

            #Otherwise generate linear x axis
            else:
                x_array = range(0,len(data[:,i]))

        #If a Step splot is requested
        if(stepshape==1):
            if(subplot==0):
                plt.step(x_array,y_array,color=viridis(i),where='post',alpha=alpha)
            else:
                ax.step(x_array,y_array,color=viridis(i),where='post',alpha=alpha)

        #Otherwise it's a Line plot
        else:
            if(subplot==0):
                plt.plot(x_array,y_array,color=viridis(i),alpha=alpha)
            else:
                ax.plot(x_array,y_array,color=viridis(i),alpha=alpha)

        #If legend is requested, append element with label
        if(legend==1 and subplot==0):
            legend_elements.append(Line2D([0],[0], marker='s', color='w', label=legendlabel+" "+str(i),markerfacecolor=viridis(i), markersize=15))
    
    #Only if not a subplot
    if(subplot==0):

        #If legend is requested, crete legend
        if(legend==1):
            plt.legend(handles=legend_elements, loc='lower right')

        #Save image if requested
        if(save==1):
            plt.savefig(filename, format='svg')

        #Show image if requested
        if(show==1):
            plt.show()

#%%

# --------------------------
# MULTIPLE SUBPLOT FUNCTION
# --------------------------
#
# DESCRIPTION: it creates a plot with multiple subplots from MultiLinePlots.
#
# INPUT ARGUMENTS
#
# -data        -> list of vectors with the data values to plot
# -n_lines     -> number of lines to plot on each subplot
#
# -x_axis      -> list of vector with x-coordinates (optional), should have the same size as data list
# -stepshape   -> 1 for Step Plot, 0 for Line Plot
#
# -show        -> 1 if the image must be shown in screen
#
# -x_label     -> label that will appear on the x-axis
# -x_ax_lim    -> list with the limit values of the x-axis (min,max)
# -y_label     -> label that will appear on the y-axis
# -y_ax_lim    -> list with the limit values of the y-axis (min,max)
#
# -title       -> Title that will appear on the graph
# -size        -> Size of the graph (x,y)
# -cmap        -> Color map being used to differentiate lines
# -save        -> 1 if the image must be saved into a .svg file
# -filename    -> Name that will be given to the image file
#

def MultipleSubplot(data, n_lines, x_axis=[], stepshape=0, show=1, x_label="X_label", x_ax_lim = [], y_label="Y_label", y_ax_lim = [], cmap='RdYlGn', title="Title", size=(15,10), save=0, filename="test.svg"):

    n_subplots = data.shape[0]

    if(n_subplots>8):
        print("PLOTING ERROR: Too many subplots. Max 8.")
    else:
        n = int(math.ceil(n_subplots/2))
        if(n>0):
            m = int(math.ceil(n_subplots/n))
        else:
            m = 1

    fig, axs = plt.subplots(m, n, sharex=True, sharey=True, figsize=size)

    #Configure Plot

    fig.suptitle(title, fontsize=16)

    for ax in axs.flat:
        ax.set(xlabel=x_label, ylabel=y_label)

        if(len(x_ax_lim)==2):
            ax.set_xlim(x_ax_lim)

        if(len(y_ax_lim)==2):
            ax.set_ylim(y_ax_lim)

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    for splot in range(0,n_subplots):

        if(len(x_axis)>1):
            if(n==1):
                MultiLinePlot(data[splot], n_lines, x_axis=x_axis[splot], stepshape=0, show=0, subplot=1, ax=axs[int(splot/n)], x_label="", x_ax_lim = [], y_label="", y_ax_lim = [], legend=0, cmap='RdYlGn', save=0)
                axs[int(splot/n)].set_title("Profile "+str(splot))
            else:
                MultiLinePlot(data[splot], n_lines, x_axis=x_axis[splot], stepshape=0, show=0, subplot=1, ax=axs[int(splot/n),int(splot%n)], x_label="", x_ax_lim = [], y_label="", y_ax_lim = [], legend=0, cmap='RdYlGn', save=0)
                axs[int(splot/n),int(splot%n)].set_title("Profile "+str(splot))

        else:
            if(n==1):
                MultiLinePlot(data[splot], n_lines, x_axis=[], stepshape=0, show=0, subplot=1, ax=axs[int(splot/n)], x_label="", x_ax_lim = [], y_label="", y_ax_lim = [], legend=0, cmap='RdYlGn', save=0)
                axs[int(splot/n)].set_title("Profile "+str(splot))
            else:
                MultiLinePlot(data[splot], n_lines, x_axis=[], stepshape=0, show=0, subplot=1, ax=axs[int(splot/n),int(splot%n)], x_label="", x_ax_lim = [], y_label="", y_ax_lim = [], legend=0, cmap='RdYlGn', save=0)
                axs[int(splot/n),int(splot%n)].set_title("Profile "+str(splot))

    #Save image if requested
    if(save==1):
        fig.savefig(filename, format='svg')

    #Show image if requested
    if(show==1):
        plt.show()

#%%

# --------------------------
# COLOURED MAP PLOT FUNCTION
# --------------------------
#
# DESCRIPTION: it creates a colored scatter-plot maps from 3 vectors: x positions, y positions and
#              the quantity of interest (color vector).
#
# INPUT ARGUMENTS
#
# -x_axis      -> vector with x-coordinates
# -y_axis      -> vector with y-coordinates
# -col_axis    -> vector with color coordinates (data of interest)
#
# -col_range   -> range (min,max) of the color values
# -x_label     -> label that will appear on the x-axis
# -y_label     -> label that will appear on the y-axis
#
# -colorbar    -> 1 for plot with colorbar, 0 for plot with legend (continuous colors vs discrete colors)
# -Nlegend     -> Number of entries of the legend (only relevant if colorbar=0)
# -color_label -> List with the labels to insert into the colorbar/legend. If colorbar=1 the number of
#                 entries must be equal to Nlegend
#
# -title       -> Title that will appear on the graph
# -size        -> Size of the graph (x,y)
# -cmap        -> Color map being used
# -markersize  -> Size of the markers for the Scatter plot
# -save        -> 1 if the image must be saved into a .svg file
# -show        -> 1 if the image must be shown in screen
# -filename    -> Name that will be given to the image file
#
# OUTPUT ARGUMENTS (only required if animation is used)
#
# -fig         -> Pointer to figure generated
# -scatter     -> Pointer to scatter plot generated

def ColourMap(x_axis, y_axis, col_axis, col_range=(0,1), x_label="X_label", y_label="Y_label", colorbar=1, Nlegend=3, color_label=['Low', 'Medium', 'High'], title="Title", size=(15,10),cmap='RdYlGn',markersize=5,save=0,show=0,filename="test.svg", internal=False):

    #Configure Scatter Plot
    fig = plt.figure(figsize=size)
    plt.title(title, fontsize=16)
    plt.xlabel(y_label, fontsize=12)
    plt.ylabel(x_label, fontsize=12)
    
    #Create Scatter Plot
    scatter = plt.scatter(x_axis,y_axis, c=col_axis, cmap=cmap, marker='s',s=markersize, vmin=col_range[0], vmax=col_range[1])
    
    #Setup Colorbar if requested
    if(colorbar==1):
        min_col = col_range[0]+0.001
        max_col = col_range[1]-0.001
        cbar = plt.colorbar(ticks=[min_col, 0.5*(min_col+max_col), max_col])
        cbar.ax.set_yticklabels(color_label)
        
    #Alternatively, setup Legend
    else:
        
        #Get color scheme for legend
        viridis = cm.get_cmap(cmap, Nlegend)
        
        legend_elements = []
        
        for i in range(0,Nlegend):
            legend_elements.append(Line2D([0],[0], marker='s', color='w', label=color_label[i],markerfacecolor=viridis(i), markersize=15))
        
        plt.legend(handles=legend_elements, loc='upper left')
    
    #Save image if requested
    if(save==1):
        plt.savefig(filename, format='svg')
    
    #Show image if requested
    if(show==1):
        plt.show()

    #Return values for animation
    if internal is True:
        return fig, scatter

#%%

# --------------------------
# COLOURED MAP ANIMATION FUNCTION
# --------------------------
#
# DESCRIPTION: it generates a .gif file from a series of coloured maps.
#              NOTE: it does not display the animation, but the .gif is correctly created.
#              Look at the file to see the output, not at the image displayed.
#
# INPUT ARGUMENTS
#
# -numframes   -> number of frames of the animation (aka number of iterations)
#
# -x_axis      -> vector with x-coordinates
# -y_axis      -> vector with y-coordinates
# -col_matrix  -> 2D array with the color coordinates of all iterations (data of interest)
#
# -dlyfactor   -> delay factor to scale up the time between frames of the .gif
#
# (the following arguments are inherited from ColourMap())
#
# -col_range   -> range (min,max) of the color values
# -x_label     -> label that will appear on the x-axis
# -y_label     -> label that will appear on the y-axis
#
# -colorbar    -> 1 for plot with colorbar, 0 for plot with legend (continuous colors vs discrete colors)
# -Nlegend     -> Number of entries of the legend (only relevant if colorbar=0)
# -color_label -> List with the labels to insert into the colorbar/legend. If colorbar=1 the number of
#                 entries must be equal to Nlegend
#
# -title       -> Title that will appear on the graph
# -size        -> Size of the graph (x,y)
# -cmap        -> Color map being used
# -markersize  -> Size of the markers for the Scatter plot
# -filename    -> Name that will be given to the .gif file
#

def AnimateColourMap(numframes, x_axis, y_axis, col_matrix, dlyfactor=1, col_range=(0,1), x_label="X_label", y_label="Y_label", colorbar=1, Nlegend=3, color_label=['Low', 'Medium', 'High'], title="Title", size=(15,10),cmap='RdYlGn',markersize=5,filename="test.gif"):
        
    #Implement the initial figure
    fig, scatter = ColourMap(x_axis, y_axis, col_matrix[0], col_range=col_range, x_label=x_label, y_label=y_label, colorbar=colorbar, Nlegend=Nlegend, color_label=color_label, title=title, size=size, cmap=cmap, markersize=markersize, save=0, internal=True)
        
    #Create animation and save .gif
    ani = animation.FuncAnimation(fig, update_plot, frames=range(int(numframes*dlyfactor)),fargs=(col_matrix, scatter, dlyfactor),blit=True)
    ani.save(filename, writer='imagemagick')

# Auxiliary function to create the Animation
def update_plot(i, data, scat, dlyfactor):
    k = int(i/dlyfactor)
    scat.set_array(data[k])
    return scat,

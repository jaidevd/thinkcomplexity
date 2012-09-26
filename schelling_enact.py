#!/usr/bin/env python

# A python script that simulates Schellings model of a city and animates with
# enact

import numpy as np
from time import sleep
from chaco.api import Plot, ArrayPlotData
from traits.api import HasTraits, List, Tuple, Array, Instance, Int
from traitsui.api import View, Item
from enable.component_editor import ComponentEditor


# Creating an empty array and filling it up with values indicating red houses,
# blue houses and empty sites.

x = np.zeros((100,100))

red_sites = []

for i in range(4500):
    coords = (np.random.randint(0,100),np.random.randint(0,100))
    red_sites.append(coords)

blue_sites = []
site_count = 0

while site_count < 4500:
    coords = (np.random.randint(0,100),np.random.randint(0,100))
    if coords not in red_sites:
        blue_sites.append(coords)
        site_count += 1

#blue_sites, red_sites = map(np.array, [blue_sites, red_sites])

for a,b in red_sites:
    x[a,b] = 1
for a,b in blue_sites:
    x[a,b] = -1

all_agents = red_sites
for agent in blue_sites:
    all_agents.append(agent)

print "Done defining prelimns...\n"

# Start the simulation

#def get_neighbours(agent_coords):
#    '''
#    Returns a list of tuples containing the coordinates of the neighbours
#    '''
#    
#    x_, y_ = agent_coords
#    
#    
#    if (x_ in range(1,99)) and (y_ in range(1,99)):
#        neighbour_coords = [
#            (x_+1,y_),(x_, y_+1),(x_-1, y_),(x_, y_-1)
#        ]
#    elif agent_coords in [(0,0),(0,99),(99,0),(99,99)]:
#        # agent is on one of the corners
#        if agent_coords == (0,0):
#            neighbour_coords = [(0,1),(1,0)]
#        elif agent_coords == (0,99):
#            neighbour_coords = [(0,98),(1,99)]
#        elif agent_coords == (99,0):
#            neighbour_coords = [(98,0),(99,1)]
#        else:
#            neighbour_coords = [(99,98),(98,99)]
#    else:
#        # agent is on one of the edges
#        if x_ == 0:
#            neighbour_coords = [(0,y_-1),(1, y_),(0, y_+1)]
#        elif x_ == 99:
#            neighbour_coords = [(99,y_-1),(98, y_),(99, y_+1)]
#        if y_ == 0:
#            neighbour_coords = [(x_-1, 0),(x_, 1),(x_+1, 0)]
#        elif y_ == 99:
#            neighbour_coords = [(x_-1, 99),(x_, 98),(x_+1, 99)]
#    
#    return neighbour_coords
#
#
#def ishappy(agent_coords, x):
#    '''
#    Checks whether an agent is happy
#    '''
#    
#    agent_state = x[agent_coords]
#    neighbour_coords = get_neighbours(agent_coords)
#    neighbour_states = []
#    for neighbour in neighbour_coords:
#        neighbour_states.append(x[neighbour])
#    
#    if neighbour_states.count(agent_state) >1:
#        return True
#    
#    return False
#
#def move_to_empty_cell(agent_coords, x):
#    
#    agent_state = x[agent_coords]
#    x[agent_coords] = 0
#    
#    for a in range(x.shape[0]):
#        for b in range(x.shape[1]):
#            if x[a,b] == 0:
#                x[a,b] = agent_state
#                break
#
#print "Done defining methods... \n"


class SchellingModel(HasTraits):
    x = Array
    plot = Instance(Plot)
    agent_coords = Tuple
    plotdata = ArrayPlotData
    all_agents = List
    sim_count = Int
    view = View(Item('plot', editor=ComponentEditor(), show_label=False,
                     resizable=True))
    
    def __init__(self, x, all_agents):
        
        self.x = x
        self.all_agents = all_agents
        self.plotdata = ArrayPlotData(imagedata=self.x)
        plot = Plot(self.plotdata)
        plot.img_plot('imagedata')
        self.plot = plot
        self.sim_count = 0
    
    def get_neighbours(self, agent_coords):
        x_, y_ = agent_coords
    
    
        if (x_ in range(1,99)) and (y_ in range(1,99)):
            neighbour_coords = [
                (x_+1,y_),(x_, y_+1),(x_-1, y_),(x_, y_-1)
            ]
        elif agent_coords in [(0,0),(0,99),(99,0),(99,99)]:
            # agent is on one of the corners
            if agent_coords == (0,0):
                neighbour_coords = [(0,1),(1,0)]
            elif agent_coords == (0,99):
                neighbour_coords = [(0,98),(1,99)]
            elif agent_coords == (99,0):
                neighbour_coords = [(98,0),(99,1)]
            else:
                neighbour_coords = [(99,98),(98,99)]
        else:
            # agent is on one of the edges
            if x_ == 0:
                neighbour_coords = [(0,y_-1),(1, y_),(0, y_+1)]
            elif x_ == 99:
                neighbour_coords = [(99,y_-1),(98, y_),(99, y_+1)]
            if y_ == 0:
                neighbour_coords = [(x_-1, 0),(x_, 1),(x_+1, 0)]
            elif y_ == 99:
                neighbour_coords = [(x_-1, 99),(x_, 98),(x_+1, 99)]
        
        return neighbour_coords
    
    def ishappy(self, agent_coords):
        '''
        Checks whether an agent is happy
        '''
        
        agent_state = self.x[agent_coords]
        neighbour_coords = self.get_neighbours(agent_coords)
        neighbour_states = []
        for neighbour in neighbour_coords:
            neighbour_states.append(self.x[neighbour])
        
        if neighbour_states.count(agent_state) >1:
            return True
        
        return False
    
    def move_to_empty_cell(self, agent_coords):
        agent_state = self.x[agent_coords]
        self.x[agent_coords] = 0

        while True:
            a = np.random.randint(0,100)
            b = np.random.randint(0,100)
            if self.x[a,b] == 0:
                self.x[a,b] = agent_state
                return
    
    def run_simulation(self):
        sim_count = 0
        for i in range(100):
            for agent in self.all_agents:
                if not self.ishappy(agent):
                    self.move_to_empty_cell(agent)
                    sim_count += 1
                    #print sim_count
                    if sim_count%500 == 0:
                        
                        self.plotdata.set_data('imagedata', self.x)
                        self.plot.request_redraw()
                        print 'Image Drawn', sim_count
                        sleep(2)
    
    def check_allhappy(self):
        for a in range(self.x.shape[0]):
            for b in range(self.x.shape[1]):
                if self.x[a,b]!=0.0:
                    if not self.ishappy((a,b)):
                        return False
        return True

print "Done defining traits class...\n"

#if __name__ == '__main__':
#    sm = SchellingModel(x, all_agents)
#    print 'Initialized class object...\n'
#    sm.configure_traits()
#    print 'Object.configured_traits...\n'
#    print 'Running Simulation...\n'
#    sm.run_simulation()
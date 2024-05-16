#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:28:26 2024

@author: boyalin
"""

from numpy import random, mean

params = {'world_size':(20,20),
          'num_agents':380,
          'same_pref' :0.4,
          'max_iter'  :100,
          'out_path'  :r'/Users/boyalin/Documents/GitHub/python1_lab9b/abm_results.csv' }

class Agent():
    def __init__(self, world, same_pref):
        self.world = world
        self.same_pref = same_pref

    def move(self): 
        vacancies = self.world.find_vacant(return_all=True) 
        for patch in vacancies: 
            self.i_moved = True

class World():
    def __init__(self, params):
        assert(params['world_size'][0] * params['world_size'][1] > params['num_agents']), 'Grid too small for number of agents.'
        self.params = params
        self.reports = {}

        self.grid     = self.build_grid(params['world_size'])
        self.agents   = self.build_agents(params['num_agents'], params['same_pref'])

        self.init_world()

    def build_grid(self, world_size):
        """create the world that the agents can move around on"""
        locations = [(i,j) for i in range(world_size[0]) for j in range(world_size[1])]
        return {l:None for l in locations}

    def build_agents(self, num_agents, same_pref):
        """generate a list of Agents that can be iterated over"""

        agents = [Agent(self, same_pref) for i in range(num_agents)]
        random.shuffle(agents)
        return agents

    def init_world(self):
        """a method for all the steps necessary to create the starting point of the model"""

        for agent in self.agents:
            loc = self.find_vacant()
            self.grid[loc] = agent
            agent.location = loc

        assert(all([agent.location is not None for agent in self.agents])), "Some agents don't have homes!"
        assert(sum([occupant is not None for occupant in self.grid.values()]) == self.params['num_agents']), 'Mismatch between number of agents and number of locations with agents.'

        #set up some reporting dictionaries
        self.reports['integration'] = []

    def find_vacant(self, return_all=False):
        """finds all empty patches on the grid and returns a random one, unless kwarg return_all==True,
        then it returns a list of all empty patches"""

        empties = [loc for loc, occupant in self.grid.items() if occupant is None]
        if return_all:
            return empties
        else:
            choice_index = random.choice(range(len(empties)))
            return empties[choice_index]

    def run(self):
        """handle the iterations of the model"""
        log_of_moved = []
        
        self.report_integration()
        log_of_moved.append(0) #no one moved at startup

        for iteration in range(self.params['max_iter']):

            random.shuffle(self.agents) #randomize agents before every iteration
            move_results = [agent.move() for agent in self.agents]
            num_moved = sum([r==1 for r in move_results])
            log_of_moved.append(num_moved)
            
        self.reports['log_of_moved'] = log_of_moved
        self.report()

    def report(self, to_file=True):
        """report final results after run ends"""
        reports = self.reports

        print('\nAll results begin at time=0 and go in order to the end.\n')
        print('The number of moves per turn:', reports['log_of_moved'])

        if to_file:
            out_path = self.params['out_path']
            with open(out_path, 'w') as f:
                headers = 'turn,num_moved\n'
                f.write(headers)
                for i in range(len(reports['log_of_happy'])):
                    line = ','.join([str(i),
                                     str(reports['log_of_moved'][i]),
                                     '\n'
                                     ])
                    f.write(line)
            print('\nResults written to:', out_path)

world = World(params)
world.run()
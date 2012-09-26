#!/usr/bin/env python

import numpy as np
from schelling_enact import SchellingModel

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


sm = SchellingModel(x, all_agents)
sm.configure_traits()

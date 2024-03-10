from biased_walker import BiasedWalker
from random_angle_walker import RandomAngleWalker
from straight_walker import StraightWalker
from grid import Grid
from simulation import Simulation
import numpy as np
import graph

walker = StraightWalker(True)
grid = Grid("config\\obstacles.json", "config\\teleporters.json")

sim = Simulation(grid, "test.json")
sim.simulate(walker)
sim.graph()

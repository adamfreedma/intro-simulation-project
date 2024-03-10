from biased_walker import BiasedWalker
from random_angle_walker import RandomAngleWalker
from straight_walker import StraightWalker
from grid import Grid
from simulation import Simulation
import numpy as np
from screen import Screen
import graph
import threading

walker = RandomAngleWalker(True)
grid = Grid("config\\obstacles.json", "config\\teleporters.json")
screen = Screen(800, 600)

ui_thread = threading.Thread(target=screen.run, daemon=True)
ui_thread.start()

sim = Simulation(grid, screen, "test.json")
sim.simulate(walker)
sim.graph()

import matplotlib.pyplot as plt
import numpy as np
import json


def read_json(path: str):
    with open(path, 'r') as f:
        return json.load(f)

def distance_graph(data_path: str, output_path: str):
    
    data = read_json(data_path)["distance"]

    fig, ax = plt.subplots()
    ax.plot(range(len(data)), data)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig(output_path)
    plt.show()
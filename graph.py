import matplotlib.pyplot as plt # type: ignore[import]
import matplotlib
import numpy as np
import json
from typing import Dict, Any

matplotlib.use('Agg')

def read_json(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return dict(json.load(f))

def distance_graph(data_path: str, output_path: str, axis: str="") -> None:
    
    data = read_json(data_path)[f"{axis}distance"]

    fig, ax = plt.subplots()
    ax.plot(range(len(data)), data)

    ax.set(xlabel='Steps', ylabel='Distance',
        title=f"Average {axis}distance as a function of steps")
    ax.grid()

    fig.savefig(f"{output_path}-{axis}distance.png")
    plt.close(fig)
    
def cross_amount_graph(data_path: str, output_path: str) -> None:
    
    data = read_json(data_path)["y_cross_count_list"]

    fig, ax = plt.subplots()
    ax.plot(range(len(data)), data)

    ax.set(xlabel='Steps', ylabel='Y cross count',
        title='Average Y axis cross count as a function of steps')
    ax.grid()

    fig.savefig(f"{output_path}-cross-count.png")
    plt.close(fig)
import matplotlib.pyplot as plt  # type: ignore[import]
import matplotlib
import numpy as np
import json
from typing import Dict, Any

matplotlib.use("Agg")

import json
from typing import Dict, Any


def read_json(path: str) -> Dict[str, Any]:
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(path, "r") as f:
        return dict(json.load(f))


def distance_graph(data_path: str, output_path: str, axis: str = "") -> None:
    """
    Generate a distance graph based on the logged data.

    Parameters:
        data_path (str): The path to the log file.
        output_path (str): The path to save the generated graph.
        axis (str): The axis to plot the distance against. Default is an empty string.
    """
    # reads the data
    data = read_json(data_path)[f"{axis}distance"]
    # draws the graph
    fig, ax = plt.subplots()
    ax.plot(range(len(data)), data)
    # sets the labels and title
    ax.set(
        xlabel="Steps",
        ylabel="Distance",
        title=f"Average {axis}-distance as a function of steps",
    )
    ax.grid()
    # saves the graph
    fig.savefig(f"{output_path}-{axis}distance.png")
    plt.close(fig)


def cross_count_graph(data_path: str, output_path: str) -> None:
    """
    Generate a graph showing the average Y axis cross count as a function of steps.

    Parameters:
        data_path (str): The path to the log file containing the data.
        output_path (str): The path to save the generated graph.
    None
    """
    # reads the data
    data = read_json(data_path)["y_cross_count_list"]
    # draws the graph
    fig, ax = plt.subplots()
    ax.plot(range(len(data)), data)
    # sets the labels and title
    ax.set(
        xlabel="Steps",
        ylabel="Y cross count",
        title="Average Y axis cross count as a function of steps",
    )
    ax.grid()
    # saves the graph
    fig.savefig(f"{output_path}-cross-count.png")
    plt.close(fig)
    

def time_to_leave_graph(data_path: str, output_path: str) -> None:
    """
    Generate a graph showing the time to leave a function of the simulation index.

    Parameters:
        data_path (str): The path to the log file containing the data.
        output_path (str): The path to save the generated graph.
    None
    """
    # reads the data
    data = read_json(data_path)["time_to_leave"]
    # draws the graph
    fig, ax = plt.subplots()
    ax.plot(range(len(data)), data)
    # sets the labels and title
    ax.set(
        xlabel="Simulation index",
        ylabel="Time to leave",
        title="Time to leave as a function of the simulation index",
    )
    ax.grid()
    # saves the graph
    fig.savefig(f"{output_path}-time-to-leave.png")
    plt.close(fig)

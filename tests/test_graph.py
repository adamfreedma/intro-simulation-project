import pytest
import json
from graph import read_json, distance_graph, cross_count_graph
import os

@pytest.fixture
def tmp_path() -> str:
    return "temp.png"

@pytest.fixture
def sample_data_path(tmp_path: str) -> str:
    # Create a temporary JSON file with sample data
    data = {
        "y_cross_count_list": [1, 2, 3, 4, 5],
        "xdistance": [1, 2, 3, 4, 5]
    }
    file_path = tmp_path + "sample_data.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return str(file_path)

def test_read_json(sample_data_path: str) -> None:
    # Test reading JSON file
    data = read_json(sample_data_path)
    assert data == {
        "y_cross_count_list": [1, 2, 3, 4, 5],
        "xdistance": [1, 2, 3, 4, 5]
    }
    
    os.remove(sample_data_path)

def test_distance_graph(tmp_path: str, sample_data_path: str) -> None:
    # Test generating distance graph
    output_path = str(tmp_path + "distance_graph")
    distance_graph(sample_data_path, output_path, axis="x")
    assert os.path.exists(f"{output_path}-xdistance.png")
    os.remove(f"{output_path}-xdistance.png")
    os.remove(sample_data_path)

def test_cross_amount_graph(tmp_path: str, sample_data_path: str) -> None:
    # Test generating cross amount graph
    output_path = str(tmp_path + "cross_amount_graph")
    cross_count_graph(sample_data_path, output_path)
    assert os.path.exists(f"{output_path}-cross-count.png")
    os.remove(f"{output_path}-cross-count.png")
    os.remove(sample_data_path)
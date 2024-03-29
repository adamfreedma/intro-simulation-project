import pytest
from graph_viewer_frame import GraphViewerFrame
import customtkinter as ctk  # type: ignore[import]
import os
from main import MainApp


@pytest.fixture
def graph_viewer_frame() -> GraphViewerFrame:
    return GraphViewerFrame(ctk.CTkTabview(ctk.CTk()).add("A"), MainApp())


def test_next_image(graph_viewer_frame: GraphViewerFrame) -> None:
    # Test the next_image method
    path_index = graph_viewer_frame.get_path_index()
    graph_viewer_frame.next_image()
    assert graph_viewer_frame.get_path_index() == path_index + 1


def test_prev_image(graph_viewer_frame: GraphViewerFrame) -> None:
    # Test the prev_image method
    path_index = graph_viewer_frame.get_path_index()
    graph_viewer_frame.prev_image()
    assert graph_viewer_frame.get_path_index() == path_index - 1


def test_update_folders_list(graph_viewer_frame: GraphViewerFrame) -> None:
    # Test the update_folders_list method
    assert graph_viewer_frame.folder_entry.cget("values") == [
        folder[0].split(GraphViewerFrame.get_folder_prefix())[-1]
        for folder in os.walk(os.getcwd())
        if folder[0].count(GraphViewerFrame.get_folder_prefix())
    ]


def test_update_paths(graph_viewer_frame: GraphViewerFrame) -> None:
    # Test the update_paths method
    graph_viewer_frame.update_paths(True)
    assert graph_viewer_frame.get_path_index() == 0


def test_update_image(graph_viewer_frame: GraphViewerFrame) -> None:
    # Test the update_image method
    assert graph_viewer_frame.image.cget("image") is None

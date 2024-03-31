from spinbox import Spinbox
import pytest
import customtkinter as ctk  # type: ignore[import]


def empty_function(_: int) -> None:
    pass


@pytest.fixture
def spinbox() -> Spinbox:
    return Spinbox(ctk.CTkFrame(ctk.CTk()), command=empty_function, min_value=5)


def test_spinbox_initialization(spinbox: Spinbox) -> None:
    assert spinbox.get() == 0


def test_spinbox_set(spinbox: Spinbox) -> None:
    spinbox.set(10)
    assert spinbox.get() == 10


def test_spinbox_add_button_callback(spinbox: Spinbox) -> None:
    spinbox.entry.delete(0, "end")
    spinbox.entry.insert(0, 10)
    spinbox.add_button_callback()

    assert spinbox.get() == 11

    spinbox.entry.insert(0, "invlaid")
    assert spinbox.add_button_callback() == False


def test_spinbox_subtract_button_callback(spinbox: Spinbox) -> None:
    spinbox.entry.delete(0, "end")
    spinbox.entry.insert(0, 10)
    spinbox.subtract_button_callback()

    assert spinbox.get() == 9

    spinbox.entry.insert(0, "invlaid")
    assert spinbox.subtract_button_callback() == False


def test_spinbox_cap_write_values(spinbox: Spinbox) -> None:
    spinbox.entry.delete(0, "end")
    spinbox.entry.insert(0, 1000)
    spinbox.entry_var.set("1000")
    spinbox.cap_write_values(spinbox.entry_var)

    assert spinbox.get() == 999

    spinbox.entry.delete(0, "end")
    spinbox.entry.insert(0, 1)
    spinbox.entry_var.set("1")
    spinbox.cap_write_values(spinbox.entry_var)

    assert spinbox.get() == 5

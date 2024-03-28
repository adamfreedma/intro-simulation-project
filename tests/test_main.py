import pytest
from main import MainApp

def test_main_app_init() -> None:
    app = MainApp()
    assert isinstance(app, MainApp)

def test_main_app_config_window() -> None:
    app = MainApp()
    app._config_window()

    assert app.height == 600
    assert app.width == 800
    
def test_main_app_close() -> None:
    app = MainApp()
    app.close()
    # Add assertions to test the close functionality

    assert app.closed == True
    
def test_main_app_confirm_menu() -> None:
    app = MainApp()
    app.confirm_menu()
    app.close_confirm_menu()

    assert app.confirm_menu_open == False
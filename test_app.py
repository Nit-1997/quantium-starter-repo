from dash.testing.application_runners import import_app
import pytest


@pytest.fixture
def dash_duo(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    yield dash_duo


def test_header_present(dash_duo):
    header = dash_duo.find_element("#header-title")
    assert header is not None
    assert header.text == "Pink Morsel Sales Visualizer"


def test_visualization_present(dash_duo):
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    chart = dash_duo.find_element("#sales-line-chart")
    assert chart is not None


def test_region_picker_present(dash_duo):
    region_picker = dash_duo.find_element("#region-filter")
    assert region_picker is not None

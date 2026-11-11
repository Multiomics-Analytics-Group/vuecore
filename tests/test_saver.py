import plotly.graph_objects as go
import pytest
from vuecore.engines.plotly.saver import save


@pytest.fixture
def figure() -> go.Figure:
    return go.Figure(go.Scatter(x=[1, 2, 3], y=[3, 1, 2]))


def test_save_writes_the_file_into_an_existing_folder(figure, tmp_path):
    # Given a destination in a folder that exists
    destination = tmp_path / "plot.html"

    # When the figure is saved there
    save(figure, str(destination))

    # Then the file is written
    assert destination.is_file()


def test_save_names_a_folder_that_does_not_exist(figure, tmp_path):
    # Given a destination in a folder that has not been created
    missing_folder = tmp_path / "plot_dir"
    destination = missing_folder / "plot.html"

    # When the figure is saved there
    with pytest.raises(FileNotFoundError) as error:
        save(figure, str(destination))

    # Then the message names the folder, and the folder is not created
    assert f"'{missing_folder}' is not an existing folder" in str(error.value)
    assert not missing_folder.exists()


def test_save_names_a_folder_that_is_a_file(figure, tmp_path):
    # Given a file where the destination's folder should be
    blocking_file = tmp_path / "plot_dir"
    blocking_file.write_text("not a folder")
    destination = blocking_file / "plot.html"

    # When the figure is saved there
    with pytest.raises(FileNotFoundError) as error:
        save(figure, str(destination))

    # Then the message names the folder
    assert f"'{blocking_file}' is not an existing folder" in str(error.value)

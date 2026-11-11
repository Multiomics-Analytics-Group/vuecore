import plotly.graph_objects as go
import pytest
from vuecore.engines.plotly.saver import save


@pytest.fixture
def figure() -> go.Figure:
    return go.Figure(go.Scatter(x=[1, 2, 3], y=[3, 1, 2]))


def test_save_creates_a_folder_that_does_not_exist_yet(figure, tmp_path):
    # Given a destination in a folder that has not been created
    destination = tmp_path / "plot_dir" / "nested" / "plot.html"

    # When the figure is saved there
    save(figure, str(destination))

    # Then the folders are created and the file is written
    assert destination.is_file()


def test_save_names_the_cause_when_the_folder_cannot_be_created(figure, tmp_path):
    # Given a file where the destination's folder should be
    blocking_file = tmp_path / "plot_dir"
    blocking_file.write_text("not a folder")
    destination = blocking_file / "plot.html"

    # When the figure is saved there
    with pytest.raises(RuntimeError) as error:
        save(figure, str(destination))

    # Then the message names the file and the error that stopped it
    message = str(error.value)
    assert str(destination) in message
    assert "FileExistsError" in message


def test_save_names_the_supported_formats_for_an_unsupported_extension(
    figure, tmp_path
):
    # Given a destination with an extension that is not a supported format
    destination = tmp_path / "plot.xyz"

    # When the figure is saved there
    with pytest.raises(RuntimeError) as error:
        save(figure, str(destination))

    # Then the message says the format is unsupported and lists the supported ones
    message = str(error.value)
    assert "Unsupported file format: '.xyz'" in message
    assert "'.html'" in message

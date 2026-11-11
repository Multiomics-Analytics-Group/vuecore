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


def test_save_names_the_folder_that_does_not_exist_and_does_not_create_it(
    figure, tmp_path
):
    # Given a destination in a folder that has not been created
    missing_folder = tmp_path / "plot_dir"
    destination = missing_folder / "plot.html"

    # When the figure is saved there
    with pytest.raises(RuntimeError) as error:
        save(figure, str(destination))

    # Then the message names the file and the folder, and the folder is not created
    message = str(error.value)
    assert str(destination) in message
    assert f"'{missing_folder}' is not an existing folder" in message
    assert not missing_folder.exists()


def test_save_names_the_folder_that_is_a_file(figure, tmp_path):
    # Given a file where the destination's folder should be
    blocking_file = tmp_path / "plot_dir"
    blocking_file.write_text("not a folder")
    destination = blocking_file / "plot.html"

    # When the figure is saved there
    with pytest.raises(RuntimeError) as error:
        save(figure, str(destination))

    # Then the message names the file and says the folder is not a folder
    message = str(error.value)
    assert str(destination) in message
    assert f"'{blocking_file}' is not an existing folder" in message


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


def test_save_names_the_cause_when_the_folder_is_not_writable(figure, tmp_path):
    # Given a folder that cannot be written to
    read_only_folder = tmp_path / "read_only"
    read_only_folder.mkdir()
    read_only_folder.chmod(0o500)
    destination = read_only_folder / "plot.html"

    # When the figure is saved there
    try:
        with pytest.raises(RuntimeError) as error:
            save(figure, str(destination))
    finally:
        read_only_folder.chmod(0o700)

    # Then the message names the file and the error that stopped it
    message = str(error.value)
    assert str(destination) in message
    assert "PermissionError" in message

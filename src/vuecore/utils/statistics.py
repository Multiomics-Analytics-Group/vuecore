import numpy as np
from scipy import stats


def get_density(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Calculates the kernel density estimate for each point in a 2D dataset.

    Parameters
    ----------
    x : np.ndarray
        The x-coordinates of the data points.
    y : np.ndarray
        The y-coordinates of the data points.

    Returns
    -------
    np.ndarray
        An array of density values, one for each input (x, y) point.
    """
    values = np.vstack([x, y])
    kernel = stats.gaussian_kde(values)
    density = kernel(values)
    return density

from logging import debug

import yaml

from .._types import PathLike


def write_ids(filename: PathLike, data: dict):
    """Write ids data to yaml file [PROOF OF CONCEPT].

    Parameters
    ----------
    filename : PathLike
        Filename to save data to.
    data : dict
        Dictionary with keys to write.
    """
    with open(filename, 'w') as f:
        yaml.dump(data, f)
    debug('wrote %r' % filename)
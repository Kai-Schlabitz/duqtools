from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Sequence, Tuple

from ._types import PathLike
from .schema.runs import Runs

if TYPE_CHECKING:
    from .ids import ImasHandle


@contextmanager
def work_directory(path: PathLike):
    """Changes working directory and returns to previous on exit.

    Parameters
    ----------
    path : PathLike
        Temporarily change to this directory.
    """
    prev_cwd = Path.cwd().resolve()
    try:
        os.chdir(path)
        yield
    finally:  # In any case, no matter what happens, go back eventually
        os.chdir(prev_cwd)


def read_imas_handles_from_file(inp: PathLike, ) -> Dict[str, ImasHandle]:
    """Read a collection of imas paths from a file.

    Input can be a `Runs.yaml` file `data.csv` file.

    The CSV file must have contain at least 5 columns, including: `user`,
    `db`, `shot`, and `run`. The first column is used as the index.
    The index can be any string or number, as long as it uniquely
    identifies the row.

    Parameters
    ----------
    inp : PathLike
        Name of the file to read.
    as_dataframe : bool, optional
        Return imas handles in a dataframe instead.

    Returns
    -------
    Union[Dict[str, ImasHandle], 'pd.DataFrame']
        Returns a dict with the Imas handles.

    Raises
    ------
    ValueError
        When the file cannot be opened.
    """
    import csv

    from .ids import ImasHandle

    inp = Path(inp)

    if inp.suffix == '.csv':
        handles = {}
        with open(inp) as f:
            reader = csv.DictReader(f)

            index_col = reader.fieldnames[0]  # type: ignore

            for row in reader:
                index = row.pop(index_col)
                handles[index] = ImasHandle(**row)

    elif inp.name == 'runs.yaml':
        runs = Runs.parse_file(inp)
        handles = {
            str(run.dirname): ImasHandle.parse_obj(run.data_out)
            for run in runs
        }

    else:
        raise ValueError(f'Cannot open file: {inp}')

    return handles


def split_paths(paths: Sequence[str]) -> Tuple[str, Tuple[str, ...]]:
    """Split paths into its common prefix and keys.

    Parameters
    ----------
    paths : Sequence[str]
        Paths that can be found in the IDS entry. Must contain
        `/*/` to denote the time component.

    Returns
    -------
    prefix, keys : Tuple[str, List[str]]
        Return the common prefix and corresponding keys.
    """

    split_paths = (path.split('/*/') for path in paths)

    prefixes, keys = zip(*split_paths)

    prefix_set = set(prefixes)
    if not len(prefix_set) == 1:
        raise ValueError(
            f'All keys must have the same prefix, got {prefix_set}')

    return prefixes[0], keys

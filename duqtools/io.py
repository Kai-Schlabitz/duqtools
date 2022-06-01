import f90nml

try:
    import imas
except ImportError:
    pass


def fetch_ids_data(
    *,
    shot: int,
    run: int,
    user_name: str,
    db_name: str,
) -> 'imas.DBEntry':
    """Fetch entry from IMAS database.

    e.g.
    ```
    db = fetch_ids_data(
        shot = 94875, run = 1, user_name = 'g2aho', db_name = 'jet')
    # -> /afs/eufus.eu/user/g/g2aho/public/imasdb/jet/3/0/ids_948750001.*

    db = fetch_ids_data(
        shot=94875, run=250, user_name='g2ssmee', db_name='jet')
    # -> /afs/eufus.eu/user/g/g2ssmee/public/imasdb/jet/3/0/ids_948750250.*
    ```

    Parameters
    ----------
    shot : int
        Shot number
    run : int
        Run number
    user_name : str
        User name
    db_name : str
        Database name

    Returns
    -------
    db : imas.DBEntry
        Imas database entry
    """
    backend = imas.imasdef.MDSPLUS_BACKEND
    db = imas.DBEntry(
        backend_id=backend,
        shot=shot,
        run=run,
        user_name=user_name,
        db_name=db_name,
    )

    return db


def read_jetto_in(path: str) -> dict:
    """Read jetto.in (fortran namelist).

    TODO: is the header in jetto.in important?

    Parameters
    ----------
    path : str
        Path to jetto.in namelist

    Returns
    -------
    namelist : f90nml.Namelist
        Returns parameters in jetto.in as Namelist
    """
    return f90nml.read(path)


def write_jetto_in(path: str, namelist: dict):
    """Write dictionary to jetto.in file.

    Parameters
    ----------
    path : str
        Path to jetto.in namelist
    namelist : dict
        Fortran namelist in dictionary format
    """
    nml = f90nml.Namelist(namelist)
    nml.write(path)

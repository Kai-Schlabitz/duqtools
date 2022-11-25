import sys
from pathlib import Path
from typing import List, Optional, Union

from pydantic import DirectoryPath, Field, validator

from ._basemodel import BaseModel
from ._description_helpers import formatter as f
from ._dimensions import CoupledDim, OperationDim
from ._imas import ImasBaseModel
from .data_location import DataLocation
from .matrix_samplers import (CartesianProduct, HaltonSampler, LHSSampler,
                              SobolSampler)
from .variables import VariableConfigModel

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal


class CreateConfigModel(BaseModel):
    """The options of the `create` subcommand are stored in the `create` key in
    the config."""
    dimensions: List[Union[CoupledDim, OperationDim]] = Field(description=f("""
        The `dimensions` specifies the dimensions of the matrix to sample
        from. Each dimension is a compound set of operations to apply.
        From this, a matrix all possible combinations is generated.
        Essentially, it generates the
        [Cartesian product](en.wikipedia.org/wiki/Cartesian_product)
        of all operations. By specifying a different `sampler`, a subset of
        this hypercube can be efficiently sampled.
        """))

    sampler: Union[LHSSampler, HaltonSampler, SobolSampler,
                   CartesianProduct] = Field(default=CartesianProduct(),
                                             discriminator='method',
                                             description=f("""
        For efficient UQ, it may not be necessary to sample the entire matrix
        or hypercube. By default, the cartesian product is taken
        (`method: cartesian-product`). For more efficient sampling of the space,
        the following `method` choices are available:
        [`latin-hypercube`](en.wikipedia.org/wiki/Latin_hypercube_sampling),
        [`sobol`](en.wikipedia.org/wiki/Sobol_sequence),
        [`halton`](en.wikipedia.org/wiki/Halton_sequence).
        Where `n_samples` gives the number of samples to extract.
        """))

    template: DirectoryPath = Field(description=f("""
        Template directory to modify. Duqtools copies and updates the settings
        required for the specified system from this directory. This can be a
        directory with a finished run, or one just stored by JAMS (but not yet
        started). By default, duqtools extracts the input IMAS database entry
        from the settings file (e.g. jetto.in) to find the data to modify for
        the UQ runs.
        """))

    template_data: Optional[ImasBaseModel] = Field(description=f("""
        Specify the location of the template data to modify. This overrides the
        location of the data specified in settings file in the template
        directory.
        """))

    data: DataLocation = Field(description=f("""
        Where to store the in/output IDS data.
        The data key specifies the machine or imas
        database name where to store the data (`imasdb`). duqtools will write the input
        data files for UQ start with the run number given by `run_in_start_at`.
        The data generated by the UQ runs (e.g. from jetto) will be stored
        starting by the run number given by `run_out_start_at`.
        """))

    jruns: Optional[DirectoryPath] = Field(description=f(
        """`jruns` defines the the root directory where all simulations are
    run for the jetto system. Because the jettos system works with relative
    directories from some root directory.

    If this variable is not specified, duqtools will look for the `$JRUNS` environment
    variable, and set it to that. If that fails, `jruns` is set to the current directory `./`

    In this way, duqtools can ensure that the current work directory is
    a subdirectory of the given root directory. All subdirectories are
    calculated as relative to the root directory.

    For example, for `rjettov`, the root directory must be set to
    `/pfs/work/$USER/jetto/runs/`. Any UQ runs must therefore be
    a subdirectory.

    """))

    runs_dir: Optional[Path] = Field(description=f(
        """Relative location from the workspace, which specifies the folder where to
    store all the created runs.

    This defaults to `workspace/duqtools_experiment_x`
    where `x` is a not yet existing integer."""))


class SubmitConfigModel(BaseModel):
    """The options of the `submit` subcommand are stored under the `submit` key
    in the config.

    The config describes the commands to start the UQ runs.
    """

    submit_script_name: str = Field(
        '.llcmd', description='Name of the submission script.')
    submit_command: str = Field('sbatch',
                                description='Submission command for slurm.')
    submit_system: Literal['prominence', 'slurm'] = Field(
        'slurm',
        description='System to submit jobs to [slurm (default), prominence]')


class StatusConfigModel(BaseModel):
    """The options of the `status` subcommand are stored under the `status` key
    in the config.

    These only need to be changed if the modeling software changes.
    """

    status_file: str = Field('jetto.status',
                             description='Name of the status file.')
    in_file: str = Field('jetto.in',
                         description=f("""
            Name of the modelling input file, will be used to check
            if the subprocess has started.
            """))

    out_file: str = Field('jetto.out',
                          description=f("""
            Name of the modelling output file, will be used to
            check if the software is running.
            """))

    msg_completed: str = Field('Status : Completed successfully',
                               description=f("""
            Parse `status_file` for this message to check for
            completion.
            """))

    msg_failed: str = Field('Status : Failed',
                            description=f("""
            Parse `status_file` for this message to check for
            failures.
            """))

    msg_running: str = Field('Status : Running',
                             description=f("""
            Parse `status_file` for this message to check for
            running status.
            """))


class MergeConfigModel(BaseModel):
    """The options of the `merge` subcommand are stored under the `merge` key
    in the config.

    These keys define the location of the IMAS data, which IDS entries
    to merge, and where to store the output.

    Before merging, all keys are rebased on (1) the same radial
    coordinate specified via `base_ids` and (2) the timestamp.
    """
    data: Path = Field('runs.yaml',
                       description=f("""
            Data file with IMAS handles, such as `data.csv` or `runs.yaml`'
            """))
    template: ImasBaseModel = Field(description=f("""
            This IMAS DB entry will be used as the template.
            It is copied to the output location.
            """))
    output: ImasBaseModel = Field(
        description='Merged data will be written to this IMAS DB entry.')
    variables: List[str] = Field(description=f("""
            This is a list of variables to be merged. This means
            that the mean and error for these data over all runs are calculated
            and written back to the ouput data location.
            """))


class ConfigModel(BaseModel):
    """The options for the CLI are defined by this model."""
    submit: SubmitConfigModel = Field(
        SubmitConfigModel(),
        description='Configuration for the submit subcommand')

    create: Optional[CreateConfigModel] = Field(
        description='Configuration for the create subcommand')

    status: StatusConfigModel = Field(
        StatusConfigModel(),
        description='Configuration for the status subcommand')

    merge: Optional[MergeConfigModel] = Field(
        description='Configuration for the merge subcommand')

    workspace: Optional[str] = Field(description='Old field, currently unused')

    extra_variables: Optional[VariableConfigModel] = Field(
        description='Specify extra variables for this run.')

    system: Literal['jetto', 'dummy', 'jetto-pythontools',
                    'jetto-duqtools'] = Field(
                        'jetto', description='backend system to use')

    quiet: bool = Field(
        False,
        description='dont output to stdout, except for mandatory prompts')

    @validator('workspace', pre=True)
    def workspace_deprecated(cls, v):
        if not v:
            from warnings import warn
            warn(f("""workspace key is Deprecated and unused, use create->jruns
            and create->runs_dir to control where runs end up"""),
                 DeprecationWarning,
                 stacklevel=2)
        return None

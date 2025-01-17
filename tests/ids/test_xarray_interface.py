from __future__ import annotations

import pytest
import xarray as xr
from idsmapping_sample_data import Sample

from duqtools.api import IDSMapping, Variable

TIME_VAR = Variable(
    name="time",
    ids="core_profiles",
    path="time",
    dims=["time"],
)


@pytest.fixture
def expected_dataset_no_index():
    return xr.Dataset.from_dict(
        {
            "coords": {"time": {"dims": ("time",), "attrs": dict(), "data": [23, 24, 25]}},
            "attrs": dict(),
            "dims": {"x": 10, "time": 3},
            "data_vars": {
                "xvar": {
                    "dims": ("x",),
                    "attrs": dict(),
                    "data": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                },
                "yvar": {
                    "dims": ("x",),
                    "attrs": dict(),
                    "data": [0, 1, 4, 9, 16, 25, 36, 49, 64, 81],
                },
            },
        }
    )


@pytest.fixture
def expected_dataset_0d():
    return xr.Dataset.from_dict(
        {
            "coords": dict(),
            "attrs": dict(),
            "dims": {"x": 1},
            "data_vars": {"xval": {"dims": ("x",), "attrs": dict(), "data": [123]}},
        }
    )


@pytest.fixture
def expected_dataset_1d():
    return xr.Dataset.from_dict(
        {
            "coords": {"time": {"dims": ("time",), "attrs": dict(), "data": [23, 24, 25]}},
            "attrs": dict(),
            "dims": {"time": 3, "x": 10},
            "data_vars": {
                "xvar": {
                    "dims": ("time", "x"),
                    "attrs": dict(),
                    "data": [
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
                        [0, 3, 6, 9, 12, 15, 18, 21, 24, 27],
                    ],
                },
                "yvar": {
                    "dims": ("time", "x"),
                    "attrs": dict(),
                    "data": [
                        [0, 1, 4, 9, 16, 25, 36, 49, 64, 81],
                        [0, 4, 16, 36, 64, 100, 144, 196, 256, 324],
                        [0, 9, 36, 81, 144, 225, 324, 441, 576, 729],
                    ],
                },
            },
        }
    )


@pytest.fixture
def expected_dataset_2d():
    return xr.Dataset.from_dict(
        {
            "coords": {"time": {"dims": ("time",), "attrs": dict(), "data": [23, 24, 25]}},
            "attrs": dict(),
            "dims": {"time": 3, "x": 5, "y": 5},
            "data_vars": {
                "xvar": {
                    "dims": ("time", "x", "y"),
                    "attrs": dict(),
                    "data": [
                        [
                            [0, 1, 2, 3, 4],
                            [5, 6, 7, 8, 9],
                            [10, 11, 12, 13, 14],
                            [15, 16, 17, 18, 19],
                            [20, 21, 22, 23, 24],
                        ],
                        [
                            [0, 2, 4, 6, 8],
                            [10, 12, 14, 16, 18],
                            [20, 22, 24, 26, 28],
                            [30, 32, 34, 36, 38],
                            [40, 42, 44, 46, 48],
                        ],
                        [
                            [0, 3, 6, 9, 12],
                            [15, 18, 21, 24, 27],
                            [30, 33, 36, 39, 42],
                            [45, 48, 51, 54, 57],
                            [60, 63, 66, 69, 72],
                        ],
                    ],
                },
                "yvar": {
                    "dims": ("time", "x", "y"),
                    "attrs": dict(),
                    "data": [
                        [
                            [0, 1, 2, 3, 4],
                            [5, 6, 7, 8, 9],
                            [10, 11, 12, 13, 14],
                            [15, 16, 17, 18, 19],
                            [20, 21, 22, 23, 24],
                        ],
                        [
                            [0, 4, 16, 36, 64],
                            [100, 144, 196, 256, 324],
                            [400, 484, 576, 676, 784],
                            [900, 1024, 1156, 1296, 1444],
                            [1600, 1764, 1936, 2116, 2304],
                        ],
                        [
                            [0, 27, 216, 729, 1728],
                            [3375, 5832, 9261, 13824, 19683],
                            [27000, 35937, 46656, 59319, 74088],
                            [91125, 110592, 132651, 157464, 185193],
                            [216000, 250047, 287496, 328509, 373248],
                        ],
                    ],
                },
            },
        }
    )


@pytest.fixture
def expected_dataset_2d_ion():
    return xr.Dataset.from_dict(
        {
            "coords": {
                "time": {"dims": ("time",), "attrs": dict(), "data": [23, 24, 25]},
            },
            "attrs": dict(),
            "dims": {"time": 3, "x": 5, "y": 5},
            "data_vars": {
                "xvar": {
                    "dims": ("time", "x", "y"),
                    "attrs": dict(),
                    "data": [
                        [
                            [0, 1, 2, 3, 4],
                            [5, 6, 7, 8, 9],
                            [10, 11, 12, 13, 14],
                            [15, 16, 17, 18, 19],
                            [20, 21, 22, 23, 24],
                        ],
                        [
                            [0, 2, 4, 6, 8],
                            [10, 12, 14, 16, 18],
                            [20, 22, 24, 26, 28],
                            [30, 32, 34, 36, 38],
                            [40, 42, 44, 46, 48],
                        ],
                        [
                            [0, 3, 6, 9, 12],
                            [15, 18, 21, 24, 27],
                            [30, 33, 36, 39, 42],
                            [45, 48, 51, 54, 57],
                            [60, 63, 66, 69, 72],
                        ],
                    ],
                },
                "ions": {
                    "dims": ("time", "ion", "x", "y"),
                    "attrs": dict(),
                    "data": [
                        [
                            [
                                [0, 1, 2, 3, 4],
                                [5, 6, 7, 8, 9],
                                [10, 11, 12, 13, 14],
                                [15, 16, 17, 18, 19],
                                [20, 21, 22, 23, 24],
                            ],
                            [
                                [0, 2, 4, 6, 8],
                                [10, 12, 14, 16, 18],
                                [20, 22, 24, 26, 28],
                                [30, 32, 34, 36, 38],
                                [40, 42, 44, 46, 48],
                            ],
                            [
                                [0, 3, 6, 9, 12],
                                [15, 18, 21, 24, 27],
                                [30, 33, 36, 39, 42],
                                [45, 48, 51, 54, 57],
                                [60, 63, 66, 69, 72],
                            ],
                        ]
                    ]
                    * 3,
                },
            },
        }
    )


@pytest.fixture
def sample_data():
    return IDSMapping(Sample)


def test_no_time_index(sample_data, expected_dataset_no_index):
    variables = [
        TIME_VAR,
        Variable(
            name="xvar",
            ids="core_profiles",
            path="nested_single_profile_1d/data/grid",
            dims=["x"],
        ),
        Variable(
            name="yvar",
            ids="core_profiles",
            path="nested_single_profile_1d/data/variable",
            dims=["x"],
        ),
    ]

    dataset = sample_data.to_xarray(variables=variables)
    xr.testing.assert_equal(dataset, expected_dataset_no_index)


def test_0d(sample_data, expected_dataset_0d):
    variables = [
        Variable(
            name="xval",
            ids="core_profiles",
            path="nested_single_val/val",
            dims=["x"],
        ),
    ]
    dataset = sample_data.to_xarray(variables=variables)

    xr.testing.assert_equal(dataset, expected_dataset_0d)


def test_1d(sample_data, expected_dataset_1d):
    variables = [
        TIME_VAR,
        Variable(
            name="xvar",
            ids="core_profiles",
            path="nested_profiles_1d/*/data/grid",
            dims=["time", "x"],
        ),
        Variable(
            name="yvar",
            ids="core_profiles",
            path="nested_profiles_1d/*/data/variable",
            dims=["time", "x"],
        ),
    ]

    dataset = sample_data.to_xarray(variables=variables)
    xr.testing.assert_equal(dataset, expected_dataset_1d)


def test_2d(sample_data, expected_dataset_2d):
    variables = [
        TIME_VAR,
        Variable(
            name="xvar",
            ids="core_profiles",
            path="nested_profiles_2d/*/data/grid",
            dims=["time", "x", "y"],
        ),
        Variable(
            name="yvar",
            ids="core_profiles",
            path="nested_profiles_2d/*/data/variable",
            dims=["time", "x", "y"],
        ),
    ]

    dataset = sample_data.to_xarray(variables=variables)
    xr.testing.assert_equal(dataset, expected_dataset_2d)


def test_2d_ion(sample_data, expected_dataset_2d_ion):
    variables = [
        TIME_VAR,
        Variable(
            name="xvar",
            ids="core_profiles",
            path="nested_profiles_2d/*/data/grid",
            dims=["time", "x", "y"],
        ),
        Variable(
            name="ions",
            ids="core_profiles",
            path="nested_profiles_2d/*/data/ions/*/variable",
            dims=["time", "ion", "x", "y"],
        ),
    ]

    dataset = sample_data.to_xarray(variables=variables)
    xr.testing.assert_equal(dataset, expected_dataset_2d_ion)


def test_empty_var_ok(sample_data):
    from duqtools.ids._mapping import EmptyVarError

    EmptyVar = Variable(
        ids="core_profiles",
        path="profiles_1d/*/empty",
        dims=("time", "x"),
        name="empty",
    )

    with pytest.raises(EmptyVarError):
        sample_data.to_xarray(variables=(EmptyVar,), empty_var_ok=False)

    dataset = sample_data.to_xarray(variables=(EmptyVar,), empty_var_ok=True)

    empty = {"coords": dict(), "attrs": dict(), "dims": dict(), "data_vars": dict()}
    assert dataset.to_dict() == empty


def test_raise_on_non_existant(sample_data):
    NonExistantVar = Variable(
        ids="core_profiles",
        path="profiles_1d/*/does/not/exist",
        dims=("time", "x"),
        name="does-not-exist",
    )

    with pytest.raises(KeyError):
        sample_data.to_xarray(variables=(NonExistantVar,), skip_empty=True)
        sample_data.to_xarray(variables=(NonExistantVar,), skip_empty=False)

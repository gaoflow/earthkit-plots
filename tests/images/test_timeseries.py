# Copyright 2024-, European Centre for Medium Range Weather Forecasts.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import earthkit.plots
from earthkit.plots import schema


def _daily_da(n_days=30, seed=0):
    """Synthetic daily temperature DataArray."""
    rng = np.random.default_rng(seed)
    times = pd.date_range("2020-01-01", periods=n_days, freq="D")
    values = 280 + 10 * np.sin(np.linspace(0, 2 * np.pi, n_days)) + rng.normal(0, 1, n_days)
    return xr.DataArray(
        values.astype(np.float32),
        dims=["time"],
        coords={"time": times},
        attrs={"units": "K", "long_name": "2m temperature", "standard_name": "air_temperature"},
        name="t2m",
    )


def _annual_da(n_years=40, seed=1):
    """Synthetic annual mean temperature DataArray for stripes."""
    rng = np.random.default_rng(seed)
    years = pd.date_range("1980-01-01", periods=n_years, freq="YS")
    # Slight warming trend + noise
    values = 287 + np.linspace(0, 1.5, n_years) + rng.normal(0, 0.3, n_years)
    return xr.DataArray(
        values.astype(np.float32),
        dims=["time"],
        coords={"time": years},
        attrs={"units": "K", "long_name": "Annual mean temperature"},
        name="t2m",
    )


# ---------------------------------------------------------------------------
# Line plots
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_timeseries_line():
    """Basic line timeseries from a daily DataArray."""
    da = _daily_da()
    chart = earthkit.plots.timeseries.line(da, units="celsius")
    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_timeseries_line_with_title():
    """Line timeseries with a title and axis labels."""
    da = _daily_da()
    chart = earthkit.plots.timeseries.line(da, units="celsius", title="{variable_name}")
    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_timeseries_line_dataset_overlay():
    """Two variables in a Dataset overlaid on a single timeseries panel."""
    da = _daily_da()
    ds = xr.Dataset({"t2m": da, "t2m_smooth": da.rolling(time=7, center=True).mean()})
    chart = earthkit.plots.timeseries.line(ds, units="celsius", overlay=True)
    return chart.fig


# ---------------------------------------------------------------------------
# Bar plots
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_timeseries_bar():
    """Bar timeseries from a monthly DataArray."""
    rng = np.random.default_rng(42)
    times = pd.date_range("2020-01-01", periods=12, freq="MS")
    values = 280 + rng.normal(0, 5, 12)
    da = xr.DataArray(
        values.astype(np.float32),
        dims=["time"],
        coords={"time": times},
        attrs={"units": "K", "long_name": "Monthly mean temperature"},
        name="t2m",
    )
    chart = earthkit.plots.timeseries.bar(da, units="celsius")
    return chart.fig


# ---------------------------------------------------------------------------
# Climate stripes
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_timeseries_stripes():
    """Climate stripes from an annual DataArray."""
    da = _annual_da()
    chart = earthkit.plots.timeseries.stripes(da, cmap="RdBu_r")
    return chart.fig

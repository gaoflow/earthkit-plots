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

import earthkit.data
import pytest

import earthkit.plots
from earthkit.plots import schema


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_xarray_contourf():
    """contourf from an xarray Dataset (NetCDF source)."""
    nc = earthkit.data.from_source("sample", "era5-monthly-mean-2t-199312.nc")
    ds = nc.to_xarray()

    chart = earthkit.plots.Map(domain="Europe")
    chart.contourf(ds, units="celsius")

    chart.legend()
    chart.coastlines()
    chart.title("{variable_name}")
    chart.gridlines()

    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_xarray_dataarray_contourf():
    """contourf from an xarray DataArray (single variable selected from Dataset)."""
    nc = earthkit.data.from_source("sample", "era5-monthly-mean-2t-199312.nc")
    ds = nc.to_xarray()

    chart = earthkit.plots.Map(domain="Europe")
    chart.contourf(ds["t2m"], units="celsius")

    chart.legend()
    chart.coastlines()
    chart.title("{variable_name}")
    chart.gridlines()

    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_healpix_xarray_grid_cells():
    """grid_cells for HEALPix data passed as an xarray DataArray (ek_grid_spec in attrs)."""
    data = earthkit.data.from_source("sample", "healpix-h128-nested-2t.grib")
    ds = data.to_xarray()
    da = ds["t2m"] if "t2m" in ds else next(iter(ds.data_vars.values()))

    chart = earthkit.plots.Map(domain="Europe")
    chart.grid_cells(da, units="celsius")

    chart.legend()
    chart.coastlines()
    chart.title()
    chart.gridlines()

    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_healpix_xarray_contourf_regrid():
    """contourf for HEALPix xarray DataArray with explicit Regrid resampling."""
    from earthkit.plots.resample import Regrid

    data = earthkit.data.from_source("sample", "healpix-h128-nested-2t.grib")
    ds = data.to_xarray()
    da = ds["t2m"] if "t2m" in ds else next(iter(ds.data_vars.values()))

    chart = earthkit.plots.Map(domain="Europe")
    chart.contourf(da, resample=Regrid(resolution=0.5), units="celsius")

    chart.legend()
    chart.coastlines()
    chart.title()
    chart.gridlines()

    return chart.fig

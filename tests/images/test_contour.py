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


def _era5_fields():
    fields = earthkit.data.from_source("sample", "era5-2t-msl-1985122512.grib").to_fieldlist()
    temperature = fields.sel({"parameter.variable": "2t"})
    pressure = fields.sel({"parameter.variable": "msl"})
    return temperature, pressure


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_contour_pressure():
    _, pressure = _era5_fields()
    chart = earthkit.plots.Map(domain="Europe")
    chart.contour(pressure, units="hPa")

    chart.coastlines()
    chart.title()
    chart.gridlines()

    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_contourf_temperature():
    temperature, _ = _era5_fields()
    chart = earthkit.plots.Map(domain="Europe")
    chart.contourf(temperature, units="celsius")

    chart.legend()
    chart.coastlines()
    chart.title()
    chart.gridlines()

    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_contourf_with_contour_overlay():
    """contourf temperature with contour pressure lines overlaid."""
    temperature, pressure = _era5_fields()
    chart = earthkit.plots.Map(domain="Europe")
    chart.contourf(temperature, units="celsius", style="auto")
    chart.contour(pressure, units="hPa", style="auto")

    chart.legend()
    chart.land()
    chart.coastlines()
    chart.title()
    chart.gridlines()

    return chart.fig

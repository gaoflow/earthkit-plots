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
def test_quiver():
    data = earthkit.data.from_source("sample", "storm_ophelia_wind_850.grib").to_fieldlist()
    chart = earthkit.plots.Map(domain=[-20, 5, 40, 59])
    chart.quiver(data)

    chart.land()
    chart.coastlines()
    chart.gridlines()

    return chart.fig


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_quiver_uv_explicit():
    """quiver with u and v passed as separate fields."""
    data = earthkit.data.from_source("sample", "storm_ophelia_wind_850.grib").to_fieldlist()
    chart = earthkit.plots.Map(domain=[-20, 5, 40, 59])
    chart.quiver(u=data[0], v=data[1])

    chart.land()
    chart.coastlines()
    chart.gridlines()

    return chart.fig

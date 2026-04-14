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
import earthkit.geo.cartography


@pytest.mark.mpl_image
@pytest.mark.mpl_image_compare(style=schema.to_stylesheet(include_style_sheet=False))
def test_plot_countries():
    countries = ["France", "Italy", "Spain"]
    shapes = earthkit.geo.cartography.country_polygons(countries, resolution=50e6)

    chart = earthkit.plots.Map(domain=countries)
    chart.coastlines(color="#DDDDDD")

    for shape in shapes:
        longitudes = [point[1] for point in shape]
        latitudes = [point[0] for point in shape]
        chart.line(x=longitudes, y=latitudes, color="red")

    chart.gridlines()

    return chart.fig

import numpy as np
import pytest
from bs4 import BeautifulSoup

import utils


def _create_soup(content: str) -> BeautifulSoup:
    return BeautifulSoup(content, "html.parser")


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """<div class="rv-count col-xs-3 col-sm-5 col-md-2">
                <span class="count-num">1,141</span> <span class="count-sm">Results</span>
            </div>""",
            1141,
        ),
        (
            """<div class="rv-count col-xs-3 col-sm-5 col-md-2">
                <span class="count-num">1,233</span> <span class="count-sm">Results</span>
            </div>""",
            1233,
        ),
    ],
)
def test_get_total_results(input: str, result: int) -> None:
    assert utils.get_total_results(_create_soup(input)) == result


"""
    <div class="unit-right"></div>
    <div class="unit-right"></div>
    <div class="unit-right"></div>
"""


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <div class="unit-right"></div>
                <div class="unit-right"></div>
                <div class="unit-right"></div>
            """,
            3,
        ),
        (
            """
                <div class="unit-right"></div>
                <div class="unit-right"></div>
            """,
            2,
        ),
    ],
)
def test_get_ad_count(input: str, result: int) -> None:
    assert utils.get_ad_count(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input_total_results, input_ad_count, result",
    [
        (1348, 20, 68),
        (1248, 20, 63),
    ],
)
def test_get_number_of_pages(input_total_results: int, input_ad_count: int, result: int) -> None:
    assert utils.get_number_of_pages(input_total_results, input_ad_count) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <span class="status">Used</span>
            """,
            "Used",
        ),
        (
            """
                <span class="status">New</span>
            """,
            "New",
        ),
    ],
)
def test_get_status(input: str, result: str) -> None:
    assert utils.get_status(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <div class="title">
                    <span class="stock-results">
                        <div class="cw-icon icon-map-pin" style="font-size: 10px;"></div>
                                Camping World of Reno -
                            Reno, NV
                    </span>
                    <span class="stock-results" style="flex: 1 1; text-align: right;"> Stock # 2183267P </span>
                </div>
            """,
            ("Camping World of Reno - Reno", "NV"),
        ),
        (
            """
                <div class="title">
                    <span class="stock-results">
                        <div class="cw-icon icon-map-pin" style="font-size: 10px;"></div>
                            Uxbridge, MA
                    </span>
                    <span class="stock-results" style="flex: 1 1; text-align: right;"> Stock # 2138661P </span>
                </div>
            """,
            ("Uxbridge", "MA"),
        ),
    ],
)
def test_get_dealership_location(input: str, result: str) -> None:
    assert utils.get_dealership_location(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <div class="title">
                    <span class="stock-results">
                        <div class="cw-icon icon-map-pin" style="font-size: 10px;"></div>
                                Camping World of Reno -
                            Reno, NV
                    </span>
                    <span class="stock-results" style="flex: 1 1; text-align: right;"> Stock # 2183267P </span>
                </div>
            """,
            "2183267P",
        ),
        (
            """
                <div class="title">
                    <span class="stock-results">
                        <div class="cw-icon icon-map-pin" style="font-size: 10px;"></div>
                            Uxbridge, MA
                    </span>
                    <span class="stock-results" style="flex: 1 1; text-align: right;"> Stock # 2138661P </span>
                </div>
            """,
            "2138661P",
        ),
        (
            """
                <div class="title">
                    <span class="stock-results">
                        <div class="cw-icon icon-map-pin" style="font-size: 10px;"></div>
                            Hillsboro, OR
                        </span>
                        <span class="stock-results" style="flex: 1 1; text-align: right;">
                            Stock # 2014892  VIN:GCE24FB0018508
                        </span>
                </div>
            """,
            "2014892",
        ),
    ],
)
def test_get_stock(input: str, result: str) -> None:
    assert utils.get_stock(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <div class="specs">
                    <div class="cw-icon icon-sleeps"></div>
                    <span>Sleeps</span>
                        5
                </div>
            """,
            5,
        ),
        (
            """
                <div class="specs">
                    <div class="cw-icon icon-sleeps"></div>
                    <span>Sleeps</span>
                        6
                </div>
            """,
            6,
        ),
    ],
)
def test_get_sleeps(input: str, result: str) -> None:
    assert utils.get_sleeps(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <span class="price-info low-price ">$77,999</span>
            """,
            77999,
        ),
        (
            """
                <span class="price-info low-price ">$78,699</span>
            """,
            78699,
        ),
    ],
)
def test_get_price(input: str, result: str) -> None:
    assert utils.get_price(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <div class="specs">
                    <div class="cw-icon icon-length"></div>
                    <span>Length <em>(ft)</em></span>
                      23 ft 6 in 
                </div>
            """,
            23 + (6 / 12),
        ),
        (
            """
                <div class="specs">
                    <div class="cw-icon icon-length"></div>
                    <span>Length <em>(ft)</em></span>
                      41 ft 0 in 
                </div>
            """,
            41 + (0 / 12),
        ),
    ],
)
def test_get_length(input: str, result: str) -> None:
    assert utils.get_length(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <div role="tabpanel" class="tab-pane show active" id="specs" aria-labelledby="specsTabLink">
                    <div class="oneSpec clearfix">
                        <h4>HORSEPOWER</h4>
                        <h5>154</h5>
                    </div>
                </div>
            """,
            154.0,
        ),
    ],
)
def test__get_horsepower_value(input: str, result: float) -> None:
    assert utils._get_horsepower(_create_soup(input)) == result


@pytest.mark.parametrize(
    "input, result",
    [
        (
            """
                <div role="tabpanel" class="tab-pane show active" id="specs" aria-labelledby="specsTabLink">
                    <div class="oneSpec clearfix">
                        <h4>RV CLASS</h4>
                        <h5>Class C</h5>
                    </div>
                    <div class="oneSpec clearfix">
                            <h4>MILEAGE</h4>
                            <h5>
                                60,500
                            </h5>
                        </div>
                    <div class="oneSpec clearfix">
                            <h4>FUEL TYPE</h4>
                            <h5>Diesel</h5>
                    </div>
                </div>
            """,
            np.nan,
        ),
    ],
)
def test__get_horsepower_empty(input: str, result: float) -> None:
    assert utils._get_horsepower(_create_soup(input)) is result

import math
import time

import numpy as np
import undetected_chromedriver as uc
from bs4 import BeautifulSoup, element


def get_total_results(s: BeautifulSoup) -> int:
    """
    Get total results for filtered data

    Parameters
    ----------
    s : BeautifulSoup
        html content

    Returns
    -------
    int
        number of results
    """
    return int(s.find("div", "rv-count").find("span", "count-num").text.replace(",", ""))  # type: ignore


def get_ad_count(s: BeautifulSoup) -> int:
    """
    Get advertisement count on page

    Parameters
    ----------
    s : BeautifulSoup
        html content

    Returns
    -------
    int
        number of ads on page
    """
    return len(s.find_all("div", "unit-right"))


def get_number_of_pages(total_results: int, ad_count: int) -> int:
    """
    Calculate total number of pages

    Parameters
    ----------
    total_results : int
        All available ads
    ad_count : int
        Number of ads on page

    Returns
    -------
    int
        Pages count for all Motorhomes
    """
    return math.ceil(total_results / ad_count)


def get_status(element: element.Tag) -> str:
    """
    Status of Motorhome

    Parameters
    ----------
    element : element.Tag
        html content

    Returns
    -------
    str
        status
    """
    return element.find("span", "status").text


def get_dealership_location(element: element.Tag) -> tuple[str, str]:
    """
    Dealership location divided on state and town

    Parameters
    ----------
    element : element.Tag
        html content

    Returns
    -------
    tuple[str, str]
        state and town
    """
    return tuple(" ".join(i.split()) for i in element.find("div", "icon-map-pin").parent.text.strip().split(","))


def get_stock(element: element.Tag) -> str:
    """
    Motorhome stock

    Parameters
    ----------
    element : element.Tag
        html content

    Returns
    -------
    str
        stock
    """
    return str(
        [i.text for i in element.find_all("span", "stock-results") if "Stock" in i.text][0]
        .split("#")[-1]
        .split("VIN")[0]
        .strip()
    )


def get_sleeps(element: element.Tag) -> float:
    """
    Available sleeps

    Parameters
    ----------
    element : element.Tag
        html content

    Returns
    -------
    float
        sleeps
    """
    sleeps = element.find("div", "icon-sleeps").parent.text.split("Sleeps")[-1].strip()
    return np.nan if sleeps == "-" else float(sleeps)


def get_price(element: element.Tag) -> float:
    """
    Motorhome price

    Parameters
    ----------
    element : element.Tag
        html content

    Returns
    -------
    float
        price
    """
    return float(element.find("span", "low-price").text.strip("$").replace(",", ""))


def get_length(element: element.Tag) -> float:
    """
    Motorhome length

    Parameters
    ----------
    element : element.Tag
        html content

    Returns
    -------
    float
        length
    """
    ft = float(element.find("div", "icon-length").parent.contents[-1].split("ft")[0].strip())
    inc = float(element.find("div", "icon-length").parent.contents[-1].split("ft")[1].split("in")[0].strip())
    return ft + inc / 12


def _get_horsepower(s: BeautifulSoup) -> float:
    """
    Motorhome horsepower

    Parameters
    ----------
    s : BeautifulSoup
        html content

    Returns
    -------
    int
        horsepower
    """
    horsepower = [i for i in s.find_all("div", "oneSpec clearfix") if "HORSEPOWER" in i.text.upper()]

    time.sleep(5)
    return float(np.nan if not horsepower else horsepower[0].h5.text)


def access_details(motorhome_data: element.Tag, fn=_get_horsepower) -> object:
    """
    Access details page for every Motorhome to get additional informations

    Parameters
    ----------
    motorhome_data : _type_
        html content
    driver : _type_
        chrome driver

    Returns
    -------
    object
        additional information
    """
    href = motorhome_data.find("a", "btn-details simulateBtn")["href"]
    url_details = f"https://rv.campingworld.com{href}"

    driver_details = uc.Chrome(use_subprocess=True)
    driver_details.get(url_details)
    soup_details = BeautifulSoup(driver_details.page_source, "lxml")

    return fn(soup_details)

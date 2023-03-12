import time

import numpy as np
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup, element

import utils

BASIC_URL = "https://rv.campingworld.com/"


# TODO readme
# TODO github


def _get_values(motorhome_data: element.Tag, price_threshold: int = 300000) -> dict[str, object]:
    """
    Get values about Motorhome

    Parameters
    ----------
    motorhome_data : element.Tag
        motorhome html description

    Returns
    -------
    dict[str, object]
        Motorhomes data save as dict
    """
    motorhome: dict[str, object] = {}
    motorhome["status"] = utils.get_status(motorhome_data)
    motorhome["stock"] = utils.get_stock(motorhome_data)
    motorhome["sleeps"] = utils.get_sleeps(motorhome_data)
    motorhome["length"] = utils.get_length(motorhome_data)
    motorhome["price"] = utils.get_price(motorhome_data)
    if motorhome["price"] > price_threshold:
        motorhome["horsepower"] = utils.access_details(motorhome_data)
    else:
        motorhome["horsepower"] = np.nan
    (
        motorhome["town"],
        motorhome["state"],
    ) = utils.get_dealership_location(motorhome_data)

    return motorhome


def get_data(fuel_type: str = "diesel", price_threshold: int = 300000) -> None:
    """
    Scrap data about Motorhomes for Sale for specific fuel_type

    Parameters
    ----------
    fuel_type : str, optional
        provides fuel type, by default "diesel"
    """

    # Create driver
    driver = uc.Chrome(use_subprocess=True)

    page_suffix = "&page={}"
    url = f"{BASIC_URL}rvclass/motorhome-rvs?fueltype={fuel_type}{page_suffix}"

    # Empty dict to save all motorhomes from every page.
    # Key is page count, value are data for specific Motorhome
    scraped_pages: dict[int, object] = {}

    # Access url for page number one.
    # Page number is needed to get information about how many motorhomes are for sell overall
    # and how many is listed on single page
    driver.get(url.format(1))

    # Parse page source to BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, "lxml")

    # All needed data are in div with class unit-right
    motorhomes = soup.find_all("div", "unit-right")

    single_page_motorhomes: list[dict[str, str | int | float]] = []
    for motorhome_data in motorhomes:
        # Get data for each motorhome and append to single_page_motorhomes list
        single_page_motorhomes.append(_get_values(motorhome_data, price_threshold))

    scraped_pages[1] = single_page_motorhomes

    # Make script sleep to not harm website
    time.sleep(5)

    # Get number of pages for all Motorhomes for Sale
    number_of_pages = utils.get_number_of_pages(utils.get_total_results(soup), utils.get_ad_count(soup))

    # Query data for all pages. Skip first page becuase data are already queried for first page
    for i in range(2, number_of_pages + 1):
        driver.get(url.format(i))

        # Parse page source to BeautifulSoup object
        soup = BeautifulSoup(driver.page_source, "lxml")

        # All needed data are in div with class unit-right
        motorhomes = soup.find_all("div", "unit-right")

        single_page_motorhomes = []
        for motorhome_data in motorhomes:
            single_page_motorhomes.append(_get_values(motorhome_data, price_threshold))

            scraped_pages[i] = single_page_motorhomes

            time.sleep(5)

    result = pd.concat(pd.DataFrame(page) for page in scraped_pages.values())

    print(f"There is: {len(result.loc[result.duplicated()])} duplicated rows")

    result.drop_duplicates().to_csv(f"./motorhomes_with_{fuel_type}.csv", index=False)


if __name__ == "__main__":
    get_data()

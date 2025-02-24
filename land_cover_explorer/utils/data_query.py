# Description: This file contains functions to download parcel data for all states in the
# STATE_PARCEL dictionary

import os
from zipfile import ZipFile

import requests as req

from land_cover_explorer.contstants.plss_files import STATE_PARCEL

def download_parcel_data():
    """
    Download parcel data for all states in the STATE_PARCEL dictionary
    """
    parcel_data = STATE_PARCEL
    for i in parcel_data:
        state, county, url = i
        file_name = f"data/{url.split('/')[-1]}"
        with req.get(url, timeout=500) as r:
            r.raise_for_status()
            with open(file_name, "wb") as output_file:
                output_file.write(r.content)
            with ZipFile(file_name, "r") as zip_file:
                zip_file.extractall(f"data/{state}_{county}_Parcel_Polygons")
        os.remove(file_name)
    return print("Parcel data downloaded successfully")

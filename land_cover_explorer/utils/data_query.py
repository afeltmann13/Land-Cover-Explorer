# Description: This file contains functions to download parcel data for all states in the
# STATE_PARCEL dictionary

import os
from zipfile import ZipFile
import tempfile as tmp
import requests as req
import geopandas as gpd

def download_zipped_data(data):
    """
    Download parcel data for all states in the STATE_PARCEL dictionary
    data: list of tuples containing state, county, and url
    """  
    for i in data:
        state, county, url = i
        file_name = f"data/{url.split('/')[-1]}"
        with req.get(url, timeout=500) as r:
            r.raise_for_status()
            with open(file_name, "wb") as output_file:
                output_file.write(r.content)
            with ZipFile(file_name, "r") as zip_file:
                zip_file.extractall(f"data/{state}_{county}_")
        os.remove(file_name)
    return print("Parcel data downloaded successfully")

def open_zipped_data(data):
    """

    Args:
        data (list of tuples): Each tuple contains state, county, and URL to the zipped data.
    """
    parcel_data = {}
    for i in data:
        state, county, url = i
        with req.get(url, timeout=500) as r:
            r.raise_for_status()
            with tmp.TemporaryFile() as tmp_file:    
                tmp_file.write(r.content)
                with tmp.TemporaryDirectory() as tmp_dir:          
                    with ZipFile(tmp_file, "r") as zip_file:
                        zip_file.extractall(tmp_dir)
                    for file in os.listdir(tmp_dir):
                        if file.endswith(".shp"):
                            file_location = os.path.join(tmp_dir, file)
                            newdata = {state: {county: gpd.read_file(file_location)}}
                            parcel_data.update(newdata)
        return parcel_data

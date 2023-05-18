#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MLOps Discovery
#

import os
import argparse
import requests
from time import time
from pathlib import Path
import pandas as pd
from pyparsing import Sequence


def read_local(file_path: str) -> Path:
    """
        Reads a local file
        Args:
            file_path:  local file            
    """
    print(F'Reading local file {file_path}')
    df_iter = pd.read_csv(file_path, iterator=True,compression="gzip", chunksize=10000) 
    if df_iter:        
        for df in df_iter:
            try:                                
                print('File headers',df.columns)                                
                print('Top 10 rows',df.head(10))            
                break
            except Exception as ex:
                print(f"Error found {ex}")
                return
                
        print(f"file was loaded {file_path}")        
    else:
        print(F"failed to read file {file_path}")

def write_local(df: pd.DataFrame, folder: str, file_name: str) -> Path:
    """
        Write DataFrame out locally 
        Args:
            df: dataframe chunk
            folder: the download data folder
            file_name: the local file name
    """

    path = Path(f"{folder}")
    if not os.path.exists(path):
        path.mkdir(parents=True, exist_ok=True)
    
    file_path = Path(f"{folder}/{file_name}")

    if not os.path.isfile(file_path):
        df.to_parquet(path, compression="gzip", engine='fastparquet')
        print('new file')
    else:
        df.to_parquet(path, compression="gzip", engine='fastparquet', append=True)        
        print('chunk appended')
        
    return file_path

def download_file(url: str, path: str, file_path: str) -> str:
    """
    Downloads a file and saves locally
     Args:
            url : The file url
            file_path : the file name
    """
    
    path = Path(f"{path}")
    if not os.path.exists(path):
        path.mkdir(parents=True, exist_ok=True)    

    response = requests.get(url)
    # Save the Parquet file locally

    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path

def etl_web_to_local(url: str, name: str, ext = 'parquet') -> None:
    """
       Download a file    
       Args:
            url : The file url
            name : the file name
   
    """
    print("From Url to local file: ",url, name)      

    # skip an existent file
    path = f"../data/"
    file_name = f"{name}.{ext}"    
    file_path = Path(f"{path}/{file_name}")
    if os.path.exists(file_path):
            read_local(file_path)            
            return
    
    download_file(url, path, file_path)
        
    df = pd.read_parquet(file_path) 
    print(df.columns)                                
    print(df.head(10))   

def main_flow(params: Sequence[str]) -> None:
    """
        Process a CSV file from a url location with the goal to understand the data structure
    """    
    url = params.url  
    prefix = params.prefix

    try:
        start_index = url.index('_')
        end_index = url.index('.parquet')
        file_name = F"{prefix}{url[start_index:end_index]}"        
        etl_web_to_local(url, file_name)
    except ValueError as ex:
        print(F"Error: {ex}")
          

if __name__ == '__main__':
    
    os.system('clear')    
    parser = argparse.ArgumentParser(description='Download data and analyze the data')
    parser.add_argument('--url', required=True, help='url of the file')
    parser.add_argument('--prefix', required=True, help='the file prefix or group name')
    args = parser.parse_args()
    
    print('running...')
    main_flow(args)
    print('end')

# download the following filestouch
# https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet
# https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet
# python3 discovery.py --url https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet --prefix yellow

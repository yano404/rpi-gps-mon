import os
import pathlib
import sqlite3

import pandas as pd
from dotenv import load_dotenv

DOTENV_FILE = pathlib.Path(__file__).resolve().parent.joinpath(".env").resolve()
load_dotenv(DOTENV_FILE)

DB_NAME = os.environ.get("DB_NAME")
DB_TABLE_NAME = os.environ.get("DB_TABLE_NAME")
DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(f"db/{DB_NAME}").resolve()


def get_gps_data(start, end):
    con = sqlite3.connect(str(DB_FILE))
    statement = f"SELECT timestamp, time, lat, lon, alt, speed FROM {DB_TABLE_NAME} WHERE timestamp > {start} AND timestamp <= {end}"
    df = pd.read_sql_query(statement, con)
    return df

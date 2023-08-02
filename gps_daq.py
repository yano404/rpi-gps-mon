import os
import pathlib
import sqlite3
import time

from dotenv import load_dotenv
from gps3 import gps3

DOTENV_FILE = pathlib.Path(__file__).resolve().parent.joinpath(".env").resolve()

load_dotenv(DOTENV_FILE)

DB_NAME = os.environ.get("DB_NAME")
DB_TABLE_NAME = os.environ.get("DB_TABLE_NAME")
DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath(f"db/{DB_NAME}").resolve()
con = sqlite3.connect(DB_FILE)
cur = con.cursor()
cur.execute(
    f"CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (timestamp, time, lat, lon, alt, speed)"
)

GPSD_HOST = os.environ.get("GPSD_HOST")
GPSD_PORT = os.environ.get("GPSD_PORT")
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect(host=GPSD_HOST, port=GPSD_PORT)
gps_socket.watch()

for new_data in gps_socket:
    if new_data:
        ts = time.time()
        data_stream.unpack(new_data)
        gps_time = data_stream.TPV["time"]
        gps_lat = data_stream.TPV["lat"]
        gps_lon = data_stream.TPV["lon"]
        gps_alt = data_stream.TPV["alt"]
        gps_speed = data_stream.TPV["speed"]
        print(gps_time)
        if gps_time != "n/a":
            cur.execute(
                f"""
                    INSERT INTO {DB_TABLE_NAME} VALUES
                    ({ts}, '{gps_time}', {gps_lat}, {gps_lon}, {gps_alt}, {gps_speed})
                """
            )
            con.commit()

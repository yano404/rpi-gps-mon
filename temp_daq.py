import os
import pathlib
import re
import sqlite3
import subprocess
import time

from dotenv import load_dotenv

DOTENV_FILE = pathlib.Path(__file__).resolve().parent.joinpath(".env").resolve()

load_dotenv(DOTENV_FILE)

TEMP_DB_NAME = os.environ.get("TEMP_DB_NAME")
TEMP_DB_TABLE_NAME = os.environ.get("TEMP_DB_TABLE_NAME")
TEMP_DB_FILE = (
    pathlib.Path(__file__).resolve().parent.joinpath(f"db/{TEMP_DB_NAME}").resolve()
)
con = sqlite3.connect(TEMP_DB_FILE)
cur = con.cursor()
cur.execute(f"CREATE TABLE IF NOT EXISTS {TEMP_DB_TABLE_NAME} (timestamp, degC, degF)")

TEMP_HOST = os.environ.get("TEMP_HOST")
TEMP_URL = f"http://{TEMP_HOST}"
CURL_COMMAND = ["curl", TEMP_URL, "--http0.9"]
TEMP_DAQ_INTERVAL = int(os.environ.get("TEMP_DAQ_INTERVAL"))

prog = re.compile("\d+\.\d+")

while True:
    ts = time.time()
    res = subprocess.run(CURL_COMMAND, stdout=subprocess.PIPE)
    retcode = res.returncode

    if res.returncode == 0:
        retstr = res.stdout.decode()
        degc, degf = [float(x) for x in prog.findall(retstr)]
        print(f"{ts} : {degc}, {degf}")
        cur.execute(
            f"""
               INSERT INTO {TEMP_DB_TABLE_NAME} VALUES
               ({ts}, {degc}, {degf})
           """
        )
        con.commit()

    time.sleep(TEMP_DAQ_INTERVAL / 1000.0)

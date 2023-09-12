rpi-gps-mon
===========

## Requirements

- python > 3.9
- pandas > 2.0.3
- plotly > 5.15.0
- dash > 2.11.1
- [gps3](https://github.com/wadda/gps3.git)

## Usage

### Installation

1. Clone this repository.
   ```sh
   git clone https://github.com/yano404/rpi-gps-mon.git
   ```
2. Install requirements.
   - using pip
     ```
     python -m pip install pandas plotly dash gps3
     ```
   - using [poetry](https://python-poetry.org/)
     ```
     cd /path/to/rpi-gps-mon
     poetry install
     ```
3. Create `.env`.
   ```
   cd /path/to/rpi-gps-mon
   cp .env.example .env
   ```
4. Edit `.env`.
   ```
   GPSD_HOST="example.com"
   GPSD_PORT=2947
   GPS_DB_NAME="gps.db"
   GPS_DB_TABLE_NAME="gps"
   TEMP_HOST="example.com"
   TEMP_DAQ_INTERVAL=1000 #msec
   TEMP_DB_NAME="temp.db"
   TEMP_DB_TABLE_NAME="temperature"
   GRAPH_INTERVAL=10000 #msec
   ```

### DAQ

#### GPS

```sh
python gps_daq.py
```

If you use poetry,

```sh
poetry run python gps_daq.py
```

#### Temperature

```sh
python temp_daq.py
# or
poetry run python temp_daq.py
```

### Start Online Monitor

```sh
python app.py
# or
poetry run python app.py
```

Visit [localhost:8050](localhost:8050) in your web browser.

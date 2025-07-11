# Polar BLE Python

## Overview

### Library/Server
  Connects to the Polar Verity Sense watch, decodes PPG and heart‐rate packets, logs raw data, and publishes real‐time heart‐rate readings to any WebSocket client.

### Wrapper/Client
  Provides a `Smartwatch` and `WeatherStation` module, which can be used to access live data as part of the relevant programming tasks (`Session_1_HR.py`, `Session_1_Weather.py`, etc.).

  "**HR**" data is retrieved by subscribing to the server’s WebSocket feed while "**Weather**"data is simulated.

## Usage

### Library/Server

- Adjust the `POLAR_DEVICE_NAME` constant in `Logger.py` to match the ID of the Polar Watch used and run the file.

### Wrapper/Client
- Run the desired "Session_" file e.g. `python Session_1_HR.py`.



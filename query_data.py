#!/usr/bin/env python3
from btlewrap.bluepy import BluepyBackend
# from btlewrap import BluepyBackend

from miflora.miflora_poller import MiFloraPoller

from miflora.miflora_poller import (
    MI_BATTERY,
    MI_CONDUCTIVITY,
    MI_LIGHT,
    MI_MOISTURE,
    MI_TEMPERATURE,
    MiFloraPoller,
)

from influxdb import InfluxDBClient

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def poll(antenna):
    """Poll data from the sensor."""
    # backend = _get_backend(args)
    poller = MiFloraPoller(antenna[1], BluepyBackend, cache_timeout=60)
    # print("Getting data from Mi Flora")
    # print(f"FW: {poller.firmware_version()}")
    # print(f"Name: {poller.name()}")
    # print("Temperature: {}".format(poller.parameter_value(MI_TEMPERATURE)))
    # print("Moisture: {}".format(poller.parameter_value(MI_MOISTURE)))
    # print("Light: {}".format(poller.parameter_value(MI_LIGHT)))
    # print("Conductivity: {}".format(poller.parameter_value(MI_CONDUCTIVITY)))
    # print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))

    json_body = [
        {
            "measurement": antenna[0],
            "fields":{
                "temperature": poller.parameter_value(MI_TEMPERATURE),
                "moisture": poller.parameter_value(MI_MOISTURE),
                "light": poller.parameter_value(MI_LIGHT),
                "conductivity": poller.parameter_value(MI_CONDUCTIVITY),
                "battery": poller.parameter_value(MI_BATTERY)
            }
        }
    ]

    print(json_body)
    return json_body

def write_to_influx(json_body):
    
    client = InfluxDBClient(host=config['Influx']['host'], port=int(config['Influx']['port']))

    client.write_points(
        json_body,
        database = "home")

if __name__ == "__main__":
    for i in config['Connector']:
        try: 
            body = poll([i, config['Connector'][i]])
            write_to_influx(body)
        except:
            pass



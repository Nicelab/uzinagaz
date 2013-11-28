#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import logging
import sys
import time

from Arduino import Arduino
#import daemon
import requests


logger = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class ArduinoDHT(Arduino):
    """ Extend the python-arduino library by addind DHT support."""

    #TODO: add value error handling on pin and model
    def dhtRead(self, pin=None, model=11):
        """ Read humidity and temperature from a DHT sensor.

        :param pin: the pin number connected to the digital pin of the DHT sensor
        :param model: the DHT model type. Accepted values are 11, 21, 22
        :return: a string with humidity and temparature separated by a space
        """
        # the 'dht' command is added to the arduino-python library
        # by our modified prototype.ino sketch
        cmd_str = "@{cmd}%{pin}%{model}$!".format(cmd="dht", pin=pin, model=model)
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n", "")
        return rd


#TODO add exceptions
def emoncms(host='localhost', path='emoncms', apikey=None, json_data=None):
    """ Post json datas to an emoncms server.

    :param host: emoncms host server name (default to 'localhost')
    :param path: emoncms path (default to 'emoncms')
    :param apikey: emoncms read and write apikey
    :param json_data: json datas to post
    """
    # emoncms is designed than we need an HTTP GET request to post datas
    url = 'http://{0}/{1}/input/post.json?apikey={2}&json={3}'.format(host, path, apikey, json_data)
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError as error:
        logger.error(error.message)
    #return r


board = ArduinoDHT()
APIKEY = '0000'

def main():

    # avoid pin 13 to read DHT on Arduino Uno
    dht_read = board.dhtRead(12, 22)
    if 'failnan' in dht_read:
        logger.error('DHT read error')
    else:
        data = dht_read.split()
        try:
            humidity = data[0]
            temperature = data[1]
            logger.info("H: {0}% T: {1}°C".format(humidity, temperature))

            # convert from string to json formated datas and post to emoncms
            json_data = json.dumps({'humidity': humidity, 'temperature': temperature})
#        emoncms(apikey=APIKEY, json_data=json_data)
        except IndexError:
            logger.error("DHT read error")

    # read COV from MQ-7 sensor
    cov_read = board.analogRead(1)
    if not cov_read:
        logger.error("COV read error")
    else:
        logger.info("COV: "+str(cov_read))

    # Read CO from MQ-135 sensor
    co_read = board.analogRead(2)
    if not co_read:
        logger.error("CO read error")
    else:
        logger.info("CO: "+str(co_read))

    time.sleep(5)

if __name__ == "__main__":
    while True:
        main()


#TODO: test https errors and exception based on responses
#TODO: maybe add timestamp
#TODO: use emoncms node ?
#TODO: add logging messages
#TODO: use a config file
#TODO: make it a python module
#TODO: add checks on results errors
#TODO daemonize
#TODO solve mixing data problem

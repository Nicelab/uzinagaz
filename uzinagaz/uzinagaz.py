# -*- coding: utf8 -*-

import time
import json

from Arduino import Arduino
import requests


class ArduinoDHT(Arduino):
    """ Extent the python-arduino library by addind DHT support."""

    #TODO: add value error handling on pin and model
    def dhtRead(self, pin=None, model=11):
        """ Read hymidity and temperature from a DHT sensor.

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
    url = 'http://{0}/{1}/input/post.json?apikey={2}'.format(host, path, apikey)
    r = requests.get(api_url, json)
    #return r


board = ArduinoDHT()

while True:
    dht_read = board.dhtRead(2, 22)
    print dht_read
    time.sleep(1)

    # convert from string to json formated datas
    data = dht_read.split()
    humidity = data[0]
    temperature = data[1]
    json_data = json.dumps({'humidity': humidity, 'temperature': temperature})

    #post to emoncms
    emoncms(apikey='', json_data=json_data)


#TODO: test https errors and exception based on responses
#TODO: maybe add timestamp
#TODO: use emoncms node ?
#TODO: add logging
#TODO: use a config file
#TODO: make it a python module
#TODO: add cheks on results errors

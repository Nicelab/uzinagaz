# -*- coding: utf8 -*-

from Arduino import Arduino
import time


class ArduinoDHT(Arduino):

    def dhtRead(self, pin=2, model=22):
        """ Read temperature"""
        cmd_str = "@{cmd}%{pin}%{model}$!".format(cmd="dht", pin=pin, model=model)
        try:
            self.sr.write(cmd_str)
            self.sr.flush()
        except:
            pass
        rd = self.sr.readline().replace("\r\n", "")
        return rd


board = ArduinoDHT()

while True:
    toto = board.dhtRead()
    print toto
    time.sleep(1)

######################
#
#class DHT(object):
#
#    def __init__(self, pin=None, type=None, count=6):
#        self.pin = pin
#        self.type = type
#        self.count = count
#
#    def begin(self):
#        pass
#
#    def readTemperature(self):
#        temperature = 99
#        return temperature
#
#    def readHumidity(self):
#        humidity = 99
#        return humidity
#
############


#board = Arduino()


#dht22 = DHT(13, 'DHT22')
#dht22.begin()


#humidity = dht22.readHumidity()
#temperature = dht22.readTemperature()

#print('Humidity: '+str(humidity)+'%')
#print('Temperature: '+str(temperature)+'°C')


#class ArduinoDHT(Arduino):
#   pass

#board = ArduinoDHT()


#board.pinMode(13, 'OUTPUT')
#board.digitalWrite(13, 'LOW')
#delay(20)
#board.digitalWrite(13, 'HIGH')
#delayMicroseconds(40)
#board.pinMode(13, 'INPUT')
#data = []
#for i in range(1000):
#    data.append(board.digitalRead(13))
#    delayMicroseconds(10)
#
#print data

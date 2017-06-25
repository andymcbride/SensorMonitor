import logging
from random import randrange

def sensor_factory(type, pin=None):
    if type is 'Adafruit_DHT_AM2302':
        return Adafruit_DHT_AM2302(pin)
    elif type is 'test':
        return GenericSensor()



class Adafruit_DHT_AM2302(object):

    def __init__(self, pin, sensor_id):
        import Adafruit_DHT
        self.pin = pin
        self.sensor_id = sensor_id
        self.logger = logging.getLogger('collector.PiSensor')

    def get_values(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.pin)
        if temperature is not None:
            temperature = "{:0.1f}".format(temperature * 9 / 5.0 + 32)
        else:
            self.logger.error("Got NONE value for temperature on pin {}".format(self.pin))
        if humidity is not None:
            humidity = "{:0.1f}".format(humidity)
        else:
            self.logger.error("Got NONE value for humidity on pin {}".format(self.pin))
        self.logger.debug("AM2302 Pin: {} Humidity: {} Temperature: {}".format(self.pin, humidity, temperature))
        return {'humidity': humidity, 'temperature': temperature}


class GenericSensor(object):

    def __init__(self, sensor_id):
        self.logger = logging.getLogger('collector.PiSensor')
        self.sensor_id = sensor_id

    def get_values(self):
        temperature = randrange(600,1100, step=1) / 10
        humidity = randrange(200,1000, step=1) / 10
        self.logger.debug("Fake Sensor Humidity: {} Temperature: {}".format(humidity, temperature))
        return {'humidity': humidity, 'temperature': temperature}
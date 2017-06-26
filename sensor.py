import logging
from random import randrange


class SensorData(object):
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.data = {}

    def __repr__(self):
        return "Sensor ID: {} Values: {}".format(self.sensor_id, self.data)

    def add_value(self, value):
        self.data.update(value)

    def get_values(self):
        return self.data



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
        value = SensorData(self.sensor_id)
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.pin)
        if temperature is not None:
            value.data += {'temperature': "{:0.1f}".format(temperature * 9 / 5.0 + 32)}
        else:
            self.logger.error("Got NONE value for temperature on pin {}".format(self.pin))
        if humidity is not None:
            value.data += {'humidity': "{:0.1f}".format(humidity)}
        else:
            self.logger.error("Got NONE value for humidity on pin {}".format(self.pin))
        self.logger.debug("AM2302 Pin: {} {}".format(self.pin, value))
        return value


class GenericSensor(object):

    def __init__(self, sensor_id):
        self.logger = logging.getLogger('collector.PiSensor')
        self.sensor_id = sensor_id

    def get_values(self):
        value = SensorData(sensor_id=None)
        value += {'temperature': randrange(600,1100, step=1) / 10}
        value += {'humidity': randrange(200,1000, step=1) / 10}
        self.logger.debug("Fake Sensor {}".format(value))
        return value
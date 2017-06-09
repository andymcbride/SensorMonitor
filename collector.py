"""
Reads data from sensors and saves to storage
"""
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import ConfigParser
from Utils import Utils
from random import randrange


logger = ''

development = Utils.is_development()

def setup_interfaces():
    import Adafruit_DHT
    import RPi.GPIO as GPIO


def get_logger(filename, when, max_files):
    logger = logging.getLogger("collector")
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(filename, when=when, backupCount=max_files)
    logger.addHandler(handler)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    return logger


def get_dbc(host, user, db):
    db = pymysql.connect(host='127.0.0.1', user='plantz', db='plantz', cursorclass=pymysql.cursors.DictCursor)
    dbc = db.cursor()
    return dbc


def get_temperature_humidity(pin):
    global logger
    logger.debug("Collecting Temperature and Humidity Data")

    if development:
        logger.debug("Faking Temperature/Humidity")
        temperature = randrange(600,1100, step=1) / 10
        humidity = randrange(200,1000, step=1) / 10

        logger.debug("Temperature: {} Humidity: {}".format(temperature, humidity))

        return temperature, humidity

    logger.debug("Loading Temperature/Humidity DHT")
    import Adafruit_DHT
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, pin)
    if temperature is not None:
        temperature = "{:0.1f}".format(temperature * 9 / 5.0 + 32)
    else:
        logger.error("Got NONE value for temperature on pin {}".format(pin))
    if humidity is not None:
        humidity = "{:0.1f}".format(humidity)
    else:
        logger.error("Got NONE value for humidity on pin {}".format(pin))
    logger.debug("Temperature: {} Humidity: {}".format(temperature, humidity))
    return temperature, humidity

def get_moisture(pin):
    global logger

    try:
        output = GPIO.input(pin)
        if output == 0:  # Returns 0 when moisture is found
            result = 1
        else:
            result = 0
        logger.info("Found moisture value {} for pin {}".format(result, pin))
    except:
        logger.exception("Unable to get moisture value from pin {}".format(pin))
        result = None
    finally:
        return result


def main():
    global logger
    config = ConfigParser.RawConfigParser()
    config.read('sensors.cfg')

    logger = get_logger(filename=config.get('logger', 'file'), max_files=config.get('logger', 'max_files'),
                        when=config.get('logger', 'when'))

    logger.info("Starting Collector")
    scheduler = BackgroundScheduler(logger=logger)
    scheduler.start()

    scheduler.add_job(get_temperature_humidity, 'interval', kwargs={'pin': 4}, seconds=60)


    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        pass

if __name__ == "__main__":
    main()


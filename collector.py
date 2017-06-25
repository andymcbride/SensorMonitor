"""
Reads data from sensors and saves to storage
"""
import time
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler
import sensor
import camera
import storage


# def setup_interfaces():
#     import Adafruit_DHT
#     import RPi.GPIO as GPIO

logger = logging.getLogger("collector")
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler('collector.log', when='W0', backupCount=5)
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)

db = storage.Storage('sensors.db')


def main():
    # config = ConfigParser.RawConfigParser()
    # config.read('sensors.cfg')


    sensor1 = sensor.sensor_factory('test', db.get_id('sensor1'))
    sensor2 = sensor.sensor_factory('test', db.get_id('sensor1'))
    cam = camera.Camera()

    logger.info("Starting Collector")
    scheduler = BackgroundScheduler(logger=logger)
    scheduler.start()
    scheduler.add_job(sensor1.get_values, 'interval', seconds=5)
    scheduler.add_job(sensor2.get_values, 'interval', seconds=5)
    scheduler.add_job(cam.take_picture,   'interval', kwargs={'filename': 'current.jpg'}, seconds=60)
    scheduler.add_job(cam.take_picture, 'cron', hour=6, minute=30, kwargs={'filename': 'date.jpg'})


    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        pass

if __name__ == "__main__":
    main()


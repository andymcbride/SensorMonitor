
class Gpio_Sensor(object):

    def __init__(self):
        import RPi.GPIO as GPIO
        self.initialized = False

    def setup(self):
        if self.initialized is False:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(MOISTURE_1, GPIO.IN)
            GPIO.setup(MOISTURE_2, GPIO.IN)

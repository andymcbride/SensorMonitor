from subprocess import call
import logging
from os.path import splitext
from datetime import datetime
from os import devnull
from time import sleep

DEVNULL = open(devnull, 'wb')


class Camera(object):

    busy = False

    def __init__(self):
        self.logger = logging.getLogger('collector.camera')
        pass

    def take_picture(self, filename, stamp=False):
        try:
            x = 0
            while self.busy is True:
                sleep(5)
                x += 1
                if x == 5:
                    self.logger.critical("Cannot get lock on Camera")
                    return
            if self.busy is not True:
                self.busy = True
            if stamp:
                name, ext = splitext(filename)
                filename = name + str(datetime.now().date()) + ext
            call(['fswebcam', '-r 1280x720', '-S 2', '--jpeg', '95', filename], stdout=DEVNULL, stderr=DEVNULL)
            self.logger.info("Saving image: {}".format(filename))
        except:
            self.logger.exception("Problem saving image: {}".format(filename))
        finally:
            self.busy = False


from pathlib2 import Path


class Utils(object):


    @staticmethod
    def is_development():
        """ check to see if we are running on rasberry pi (well really linux but good enough) """

        path = Path('/proc/cpuinfo')
        return not path.exists()

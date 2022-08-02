import logging
import os
import datetime


class Logger:
    log = logging
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    def __init__(self):
        date = datetime.datetime.now()
        path = os.path.join(self.ROOT_DIR,
                            '../logs/' + str(date.day) + '_' + str(date.month) + '_' + str(date.year) + '_debug.log')
        self.log.basicConfig(
            filename=path,
            level=logging.DEBUG,
            format=self.FORMAT
        )

    @property
    def add(self):
        return self.log

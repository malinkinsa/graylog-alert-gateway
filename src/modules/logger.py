import datetime
import logging
import sys

from os.path import abspath, dirname, join


class Logger:
    def __init__(self, logger_name='Alert Gateway', file_name='event.log'):
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)

        # File handler
        log_path = join(abspath(dirname(__file__)), f"../../logs/{file_name}")
        file_handler = logging.FileHandler(log_path, 'a')
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)

    def logging(self, message, logger_level='INFO', source=None, traceback=None):
        logging_message = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'type': logger_level,
            'message': message
        }

        if source:
            logging_message.update(source=source)

        if traceback:
            logging_message.update(traceback=traceback)

        else:
            self.logger.info(str(logging_message))


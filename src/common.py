import os
import logging


def assure_path_exists(path):
    directory = os.path.dirname(path + '/')
    if not os.path.exists(directory):
        os.makedirs(directory)


def project_root():
    return os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))


class Logger(object):
    def __init__(self, log_file_name, log_level=logging.INFO, log_mode='w'):
        assure_path_exists(os.path.join(project_root(), 'logs'))
        self.logger = logging.getLogger(log_file_name)
        log_handler = logging.FileHandler(os.path.join(project_root(), 'logs/%s.log' % log_file_name), mode=log_mode)
        formatter = logging.Formatter('%(asctime)s  %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(log_level)

    def log_message(self, conversationalist, msg):
        """Ensure message format consistency.

        :param conversationalist: who issued a message. TRACKS for chatbot or client name.
        :param msg: string
        """
        self.logger.info('%12s  %s' % (conversationalist, msg))

import os
import logging
from collections import OrderedDict


def assure_path_exists(path):
    directory = os.path.dirname(path + '/')
    if not os.path.exists(directory):
        os.makedirs(directory)


def project_root():
    return os.path.dirname(os.path.abspath(__file__))


def log_path():
    assure_path_exists(os.path.join(project_root(), 'logs'))
    return os.path.join(project_root(), 'logs')


def truck_specs_dict():
    """Ordered dict of truck specifications"""
    return OrderedDict(truck_id=None, brand=None, model=None, engine_size=None, axl_nr=None, weight=None, max_load=None)


def order_dict(client_input_dict):
    ordered_dict_values = [client_input_dict.get(param) for param, _ in truck_specs_dict().items()]
    return ordered_dict_values


def parse_event_history(log_file, history_dict):
    logger = Logger(log_file_name=log_file, log_mode='a')
    for event in history_dict:
        if event['event'] == 'user':
            logger.log_message('user', event['text'])
        elif event['event'] == 'bot':
            logger.log_message('bot', event['text'])


class Logger(object):
    def __init__(self, log_file_name, log_level=logging.INFO, log_mode='w'):
        assure_path_exists(log_path())
        self.logger = logging.getLogger(log_file_name)
        log_handler = logging.FileHandler(os.path.join(log_path(), '%s.log' % log_file_name), mode=log_mode)
        formatter = logging.Formatter('%(asctime)s  %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(log_level)

    def log_message(self, conversationalist, msg):
        """Ensure message format consistency.

        :param conversationalist: who issued a message. TRACKS for chatbot or client name.
        :param msg: string
        """
        self.logger.info('%6s  %s' % (conversationalist, msg))

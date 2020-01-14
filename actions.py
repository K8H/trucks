# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

import uuid

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from src import common


class ActionFleetSize(Action):

    logger = None

    def name(self) -> Text:
        return "action_fleet_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO entity extractor
        # print(tracker.get_latest_entity_values())
        print('ActionFleetSize')
        self.logger = common.Logger(log_file_name=tracker.latest_message['text'] + str(uuid.uuid4()), log_mode='a')
        dispatcher.utter_message(text="How many trucks are in your fleet?")

        return []


class ActionTruckIds(Action):

    fleet_size = 0

    def name(self) -> Text:
        return "action_truck_ids"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('ActionTruckIds')
        self.fleet_size = tracker.latest_message['text']
        print(self.fleet_size)
        dispatcher.utter_message(text="Please, list all %s identification numbers of your trucks.")
        return []


def get_logger():
    return ActionFleetSize.logger

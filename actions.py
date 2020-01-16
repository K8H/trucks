import csv
import os
import uuid
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from src import common

log_file_path = None
log_file_name = None


class ActionSlotReset(Action):
    def name(self):
        return 'action_slot_reset'

    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset()]


class ActionGoodbye(Action):
    def name(self):
        return 'action_goodbye'

    def run(self, dispatcher, tracker, domain):
        global log_file_path
        common.parse_event_history(log_file_name, tracker.events_after_latest_restart())
        dispatcher.utter_message(text="Thank you for your input. Your entry is stored in a csv file. Have a nice day and goodbye.")
        return[]


class ActionCompany(Action):

    def name(self) -> Text:
        return "action_company"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global log_file_path
        global log_file_name
        log_file_name = tracker.latest_message['text'] + '_' + str(uuid.uuid4())
        log_file_path = os.path.join(common.log_path(), log_file_name)

        with open(log_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list(common.truck_specs_dict().keys()))

        return []


class TruckForm(FormAction):
    """Truck form action"""

    def name(self) -> Text:
        return "truck_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["truck_id", "brand", "model", "engine_size", "axl_nr", "weight", "max_load"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "truck_id": [
                self.from_entity(entity="truck_id", intent=["inform", "request_truck"]),
                self.from_entity(entity="number")
            ],
            "brand": [
                self.from_entity(entity="brand")
            ],
            "model": [
                self.from_entity(entity="model"),
                self.from_text(intent="inform")
            ],
            "engine_size": [
                self.from_entity(entity="engine_size", intent="inform"),
                self.from_entity(entity="number")
            ],
            "axl_nr": [
                self.from_entity(entity="axl_nr", intent="inform"),
                self.from_entity(entity="number")
            ],
            "weight": [
                self.from_entity(entity="weight", intent="inform"),
                self.from_entity(entity="number")
            ],
            "max_load": [
                self.from_entity(entity="max_load", intent="inform"),
                self.from_entity(entity="number")
            ]
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Print the added truck"""
        global log_file_path

        with open(log_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(common.order_dict(tracker.slots))

        dispatcher.utter_message(template="utter_submit")
        return []

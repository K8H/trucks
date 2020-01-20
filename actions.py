import csv
import os
import uuid
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import common

log_file_path = None
log_file_name = None


class ActionSlotReset(Action):
    def name(self):
        return 'action_slot_reset'

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


class ActionGoodbye(Action):
    def name(self):
        return 'action_goodbye'

    def run(self, dispatcher, tracker, domain):
        global log_file_path
        common.parse_event_history(log_file_name, tracker.events_after_latest_restart())
        dispatcher.utter_message(
            text="Thank you for your input. Your entry is stored in a csv file. Have a nice day and goodbye.")
        return []


class CompanyForm(FormAction):

    def name(self) -> Text:
        return "company_form"

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "company": [
                self.from_entity(entity="company"),
                self.from_text()
            ]
        }

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["company"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Print the added truck"""
        global log_file_path
        global log_file_name

        log_file_name = tracker.get_slot('company') + '_' + str(uuid.uuid4())
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
                self.from_entity(entity="truck_id"),
                self.from_text()
            ],
            "brand": [
                self.from_entity(entity="brand", intent="inform"),
                self.from_text()
            ],
            "model": [
                self.from_entity(entity="model"),
                self.from_text()
            ],
            "engine_size": [
                self.from_entity(entity="engine_size"),
                self.from_text()
            ],
            "axl_nr": [
                self.from_entity(entity="axl_nr"),
                self.from_text()
            ],
            "weight": [
                self.from_entity(entity="weight"),
                self.from_text()
            ],
            "max_load": [
                self.from_entity(entity="max_load"),
                self.from_text()
            ]
        }

    @staticmethod
    def brands_list() -> List[Text]:
        """List of supported brands"""
        return ["man", "scania", "iveco", "volvo", "daimler"]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_brand(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate brand value."""

        if value.lower() in self.brands_list():
            return {"brand": value}
        else:
            dispatcher.utter_message(template="utter_wrong_brand")
            return {"brand": None}

    def validate_engine_size(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate engine size value."""
        if self.is_int(value) and 2000 < int(value) < 15000:
            return {"engine_size": value}
        else:
            dispatcher.utter_message(template="utter_wrong_engine_size")
            # validation failed, set slot to None
            return {"engine_size": None}

    def validate_axl_nr(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate axl_nr value."""
        if self.is_int(value) and 0 < int(value) < 9:
            return {"axl_nr": value}
        else:
            dispatcher.utter_message(template="utter_wrong_axl_nr")
            # validation failed, set slot to None
            return {"axl_nr": None}

    def validate_weight(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate weight value."""
        if self.is_int(value) and 1000 < int(value) < 33000:
            return {"weight": value}
        else:
            dispatcher.utter_message(template="utter_wrong_weight")
            # validation failed, set slot to None
            return {"weight": None}

    def validate_max_load(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate max load value."""
        if self.is_int(value) and 1000 < int(value) < 20000:
            return {"max_load": value}
        else:
            dispatcher.utter_message(template="utter_wrong_max_load")
            # validation failed, set slot to None
            return {"max_load": None}

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

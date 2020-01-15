import uuid
from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from src import common


class TruckForm(FormAction):
    """Truck form action"""

    logger = None

    def name(self) -> Text:
        return "truck_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        print(tracker.latest_message['text'])
        return ["truck_id", "brand", "model", "engine_size", "axl_nr", "weight", "max_load"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        print('Mapping slots')
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

    # def run(self, dispatcher: CollectingDispatcher,
    # TODO open log file only when eneter a company name
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    #     print('ActionCompany')
    #     self.logger = common.Logger(log_file_name=tracker.latest_message['text'] + str(uuid.uuid4()), log_mode='a')
    #     return []

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
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"brand": value}
        else:
            dispatcher.utter_message(template="utter_wrong_brand")
            # validation failed, set this slot to None and user will be asked for the slot again
            return {"brand": None}

    def validate_engine_size(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate engine size value."""
        if self.is_int(value) and 3000 < int(value) < 15000:
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
        if self.is_int(value) and 0 < int(value) < 6:
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
        if self.is_int(value) and 5000 < int(value) < 33000:
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
        """Print the added truck
        TODO ask if want to add another truck"""
        print('submit')
        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return []
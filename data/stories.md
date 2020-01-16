
## happy_path
* greet
  - utter_greet
  - utter_company
* response_company
    - action_company
    - truck_form
    - form{"name": "truck_form"}
    - form{"name": null}
    - utter_slots_values
    - utter_another_truck
* deny
    - utter_thankyou
    - utter_goodbye
    
## happy_path_more_trucks
* greet
  - utter_greet
  - utter_company
* response_company
    - action_company
    - truck_form
    - form{"name": "truck_form"}
    - form{"name": null}
    - utter_slots_values
    - utter_another_truck
* affirm
    - action_slot_reset
    - truck_form
    - form{"name": "truck_form"}
    - form{"name": null}
    - utter_slots_values
    - utter_another_truck
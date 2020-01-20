
## happy_path
* greet
  - utter_greet
  - utter_company
  - company_form
  - form{"name": "company_form"}
  - form{"name": null}
  - truck_form
  - form{"name": "truck_form"}
  - form{"name": null}
  - utter_slots_values
> check_correct_input

## user_correct
> check_correct_input
* deny
  - utter_correct_slots
  - slot_correct_form
  - form{"name": "slot_correct_form"}
  - form{"name": null}
  - truck_form
  - form{"name": "truck_form"}
  - form{"name": null}
  - utter_slots_values
> check_correct_input
  
## user_no_correct
> check_correct_input
* affirm
  - utter_another_input
> check_another_input
    
## user_denies
> check_another_input
* deny
    - action_goodbye
    
## user_affirms
> check_another_input
* affirm
    - action_slot_reset
    - truck_form
    - form{"name": "truck_form"}
    - form{"name": null}
    - utter_slots_values
> check_correct_input
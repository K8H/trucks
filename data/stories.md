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
> check_asked_question

## user_denies
> check_asked_question
* deny
    - action_goodbye

## user_affirms
> check_asked_question
* affirm
    - action_slot_reset
    - truck_form
    - form{"name": "truck_form"}
    - form{"name": null}
    - utter_slots_values
> check_asked_question

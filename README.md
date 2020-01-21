# Track

The aim is to implement a small interactive system (Chat Bot) to 
identify trucks, their specification and number in particular fleet.
Customer is Fleet Owner or Fleet manager.
End result of conversation should be a list of trucks with their 
specifications and numbers.
All conversations should be recorded for future analysis.

## Requirements

install rasa with 
   ```
   $ pip3 install rasa
   ```
   
and library for fuzzy string matching:
   ```
   $ pip install fuzzywuzzy[speedup]
   ```

## How to use this code?

1. Train a Rasa model inside track directory by running:
    ```
    rasa train
    ```
    The model will be stored in the `/models` directory as a zipped file.

3. Test the assistant by running:
    ```
    rasa run actions
    rasa shell -m models --endpoints endpoints.yml
    ```
    This will load the assistant in your command line for you to chat.
    
    To start the conversation just go with hi, hey or any other greeting
    you like.

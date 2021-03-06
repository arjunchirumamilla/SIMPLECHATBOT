# Simple-Chatbot

- This repository consists the python code for developing a simple chatbot.
- For demomstration the chatbot is configured for performing two tasks:
    - `Search Movie`
    - `Book Restaurant`

### Data Description:
- The `db` folder contains the data files :
    - `movies.csv`: Contains list of movies data in the below format.
       ```
       [Movie, language, Actor, Theatre_Name, genre, date, Show_Time, location]
       ```
    - `restaurants.csv`: conatins list of restaurants data in the below format.
       ```
       [cuisine, costtype, location, Restaurant]
       ```
- The `entities` folder contains the data for various entities present in each task:
    - `Search Movie`:
    ```
    [Actors, genre, date, language, location]
    ```
    - `Book Resturant`:
    ```
    [cuisine, costtype], location]
    ```
- The `intents` folder contains the data for possible user input for each intent.
- The `params` folder contains the dialog flow  to capture the required params for each intent.

### Steps to Run the Chatbot:

1. Create a python virtual environment and activate it:
    ```
    python3 -m venv bot
    source bot/bin/activate
    ```
2. Install the required libraries:
    ```
    pip install -r requirements.txt
    ```
3. Run the chatbot:
    ```
    python run.py
    ```
4. Enter `exit` once you are done.

'''
Module for chatbot.
This module implements the various tasks performed by chatbot after a
user input  which are listed below:
- Input Processing
- Intent identification
- Parameter check for current intent
- Perform action.
'''


from textblob import TextBlob
from generatengrams import ngrammatch
from Contexts import *
import json
from Intents import *
from spellcheck import *
import random
import os
import re
import pandas as pd
from termcolor import colored

def listMovies(attributes):
    return getResult(attributes, "db/movies.csv")

def listRestarunts(attributes):
    return getResult(attributes, "db/restaurants.csv")

def formatAttributes(attributes):
    message = ""
    for key in attributes:
        message = "\033[1m" + message + key + ": " + attributes[key] + "\n"
    return message

def botSays(message):
    print(colored('\033[1m' + message,'green'))

def getResult(dictAttr, filename):
    selectedData = pd.read_csv(filename)
    for col,val in dictAttr.items():
        if col != "Getconfirmation":
            selectedData = selectedData.loc[selectedData[col]==val]
    return selectedData


def check_actions(current_intent, attributes, context):
    '''This function performs the action for the intent as mentioned in the intent config file'''
    '''Performs actions pertaining to current intent for action in current_intent.actions: '''

    if current_intent == None:
        return None, context

    results = []
    if current_intent.name == "SearchMovie":
        results= listMovies(attributes)
    if current_intent.name == "BookRestaurant":
        results = listRestarunts(attributes)

    if len(results) > 0:
        message = results.to_string()
    else:
        message = "Sorry, I could not find results as per your criteria. Please try again. :("

    context = IntentComplete()
    return 'action: ' + current_intent.action + "\n" + message, context

def check_required_params(current_intent, attributes, context):
    '''Collects attributes pertaining to the current intent'''

    for para in current_intent.params:
         if para.required:
            if para.name not in attributes:
                if para.name == 'Getconfirmation':
                    if current_intent.name == "SearchMovie":
                        botSays("Please confirm if we can get the movies playing for the criteria")
                        botSays(formatAttributes(attributes))
                    elif current_intent.name == "BookRestaurant":
                        botSays("Please confirm if we can get the restaurant for the criteria")
                        botSays(formatAttributes(attributes))
                    context = Getconfirmation()
                return random.choice(para.prompts), context
    return None, context


def input_processor(user_input, context, attributes, intent):
    '''Spellcheck and entity extraction functions go here'''

    #update the attributes, abstract over the entities in user input
    attributes, cleaned_input = getattributes(user_input, context, attributes,intent)

    return attributes, cleaned_input

def loadIntent(path, intent):
    with open(path) as fil:
        dat = json.load(fil)
        intent = dat[intent]
        return Intent(intent['intentname'],intent['intentenglishname'],intent['Parameters'],intent['actions'])

def intentIdentifier(clean_input, context,current_intent):
    clean_input = clean_input.lower()
    scores = ngrammatch(clean_input)
    scores = sorted_by_second = sorted(scores, key=lambda tup: tup[1])

    if((current_intent==None) and (scores[-1][1] > 0.02)):
        return loadIntent('params/Movie_Restaurants_Params.cfg',scores[-1][0])
    else:
        # 'same intent'
        return current_intent

def getattributes(uinput,context,attributes,intent):
    '''This function marks the entities in user input, and updates the attributes dictionary'''
    #Can use context to to context specific attribute fetching
    if context.name.startswith('IntentComplete'):
        return attributes, uinput
    else:

        files = os.listdir('./entities/')
        entities = {}
        for fil in files:
            lines = open('./entities/'+fil).readlines()
            for i, line in enumerate(lines):
                lines[i] = line[:-1]
            entities[fil[:-4]] = '|'.join(lines)

        for entity in entities:
            for i in entities[entity].split('|'):
                if i.lower() in uinput.lower():
                    attributes[entity] = i
        for entity in entities:
                uinput = re.sub(entities[entity],r'$'+entity,uinput,flags=re.IGNORECASE)

        if context.name =='Getconfirmation' and context.active:

            if uinput.lower() == 'yes':
                attributes['Getconfirmation'] = uinput.lower()
                context.active = False
            if uinput.lower() == 'no':
                print("Please enter the details for the  ", intent.englishname )
                attributes ={}
                context.active = True


    return attributes, uinput

class Session:
    def __init__(self, attributes=None, active_contexts=[FirstGreeting(), IntentComplete() ]):

        '''Initialise a default session'''

        #Contexts are flags which control dialogue flow, see Contexts.py
        self.active_contexts = active_contexts
        self.context = FirstGreeting()

        #Intent tracks the current state of dialogue
        self.current_intent = None

        #attributes hold the information collected over the conversation
        self.attributes = {}

    def update_contexts(self):
        '''Not used yet, but is intended to maintain active contexts'''
        for context in self.active_contexts:
            if context.active:
                context.decrease_lifespan()

    def reply(self, raw_user_input):
        '''Generate response to user input'''

        user_input = perform_correction(raw_user_input.lower())
        #user_input = raw_user_input
        if user_input != raw_user_input:
            print("Spelling corrected: ",user_input)

        self.attributes, clean_input = input_processor(user_input, self.context, self.attributes, self.current_intent)

        self.current_intent = intentIdentifier(clean_input, self.context, self.current_intent)
        if self.current_intent == None:
            self.attributes = {}
            self.context = FirstGreeting()
            return "Sorry, I didn't get you. I can help you in searching movies and restarunts only! Your preference please"

        prompt, self.context = check_required_params(self.current_intent, self.attributes, self.context)


        #prompt being None means all parameters satisfied, perform the intent action
        if prompt is None:
            if self.context.name!='IntentComplete':
                prompt, self .context = check_actions(self.current_intent, self.attributes, self.context)

        #Resets the state after the Intent is complete
        if self.context.name=='IntentComplete':
            self.attributes = {}
            self.context = FirstGreeting()
            self.current_intent = None

        return prompt

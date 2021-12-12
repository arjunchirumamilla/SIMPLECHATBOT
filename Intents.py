'''
This Module consisits the definition of Intent class.
'''
class Intent(object):
    '''
    Intent is a special skill of chatbot for eg: booking a flight, searching
    a store etc.Each intent has few parameters(which are taken from user to
    complete an intent) and action which is performed after all the parameters
    have been fulfilled.

    Inputs:
    --------
    - name : str
        string of the intent eg: BookHotel
    - englishname: str
        corresponding identification string in english (eg: Hotel Booking)
    - params : Parameter
        list of parameters as an object of Parameter class
    - action: str
        string indicating the action performed.
    '''
    def __init__(self, name, englishname, params, action):
        self.name = name
        self.englishname = englishname
        self.action = action
        self.params = []
        for param in params:
            self.params += [Parameter(param)]

class Parameter():
    '''
    Parameters are the required information which are elicted from the user
    in order to complete the intent.

    Inputs:
    -------
    - info: dict
        Dictionary containing the below keys:
        - name:
            (str) name of the parameter
            eg: book name
        - placeholder:
            (str) value used to mask the input
            eg: $book
        - prompts:
            (str) question presented to the user.
            eg: "please enter the book name"
        - defaultprompts:
            (str) default output if the input is not understood.
            eg: Book name not understood. please renter the name.
        - required:
            (bool) importance of the parameter
            eg: True or False .
        - context:
            (str) Name of the current context
                eg: bookname_dialog_from
    '''
    def __init__(self, info):
        self.name = info['name']
        self.placeholder = info['placeholder']
        self.prompts = info['prompts']
        self.defaultprompts = info['defaultprompts']
        self.required = info['required']
        self.context = info['context']

from chatbot import Session
from termcolor import colored

session = Session()

print(colored('\033[1m' + 'BOT:','red'), colored('\033[1m'+'Hi! I can help you find movies and book restaurants. What is your preference?','green'))

while True:
    inp = input('User: ') or 'default'
    if inp == 'exit':
        print(colored('\033[1m' + 'Bye then!','red'))
        break
    else:
        print(colored('\033[1m' + 'BOT:','red'), colored('\033[1m' + session.reply(inp),'green'))

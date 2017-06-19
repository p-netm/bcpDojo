from termcolor import colored, cprint


""" print methods"""
text = colored('Hello, World!', 'green')

def p_warning(string):
    print(colored(string, 'yellow'))

def p_info(string):
    print( colored(string, 'blue'))

def p_success(string):
    print(colored(string, 'green', attrs=['dark']))

def p_danger(string):
    print(colored(string, 'red', attrs=['dark']))


"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    Dojo create_room (living_space|office) <room_name>...
    Dojo add_person <first_name> <second_name> (fellow [[yes|y]|[no|n]]|staff)
    Dojo print_room <room_name>
    Dojo print_allocations [<file_name>]
    Dojo load_people (<file_name>)
    Dojo reallocate_person (<person_id>) (<new_room_name>)
    Dojo display
    Dojo view_ids
    Dojo (-i | --interactive)
    Dojo (-h | --help | --version)

Options:
    create_room  takes in type of room and several rooms
    print_room  shows the people inside a room
    print_allocation  shows all people who have been allocated to any and all rooms
    add_person  adds a new fellow or staff
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from dojo import Dojo


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Unknown Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to the Interactive Dojo Room Allocation System!' \
        + ' (you can type help for a list of commands.)'
    prompt = '(Dojo) '

    dojo = Dojo()

    @docopt_cmd
    def do_create_room(self, arg):
        """ Usage: create_room (living_space|office) <room_name>..."""

        parsing_names_list = []
        for i in arg['<room_name>']:
            parsing_names_list.append(i.lower())
        if arg['living_space']:
            room_type = "living_space"
            self.dojo.create_room(room_type, parsing_names_list)
        elif arg['office']:
            room_type = "office"
            self.dojo.create_room(room_type, parsing_names_list)

    @docopt_cmd
    def do_add_person(self, arg):
        """ Usage: add_person <first_name> <second_name> (fellow [[yes|y]|[no|n]]|staff)"""

        # checks if fellow is set and if fellow wants accommodation or if staff is set. it then
        # passes the variables to the implementing function in the dojo object
        full_name = arg['<first_name>'] + " " + arg['<second_name>']
        if arg['fellow']:
            occupation = "fellow"
            accommodate = 'n'
            if arg['yes'] or arg['y']:
                accommodate = "yes"
            elif arg['no'] or arg['n']:
                accommodate = "no"
            self.dojo.add_person(full_name, occupation, accommodate)

        if arg['staff']:
            occupation = "staff".lower()
            self.dojo.add_person(full_name, occupation)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room_name = arg['<room_name>'].lower()
        self.dojo.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocation [<file_name>]"""

        if arg['<file_name>'] is not None:
            file_name = arg['<file_name>'].lower()
            self.dojo.print_allocations(file_name)
        else:
            self.dojo.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [<file_name>] """
        if arg['<file_name>'] is not None:
            file_name = arg['<file_name>'].lower()
            self.dojo.print_unallocated(file_name)
        else:
            self.dojo.print_unallocated()

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people (<file_name>) """
        file_name = arg['<file_name>']
        self.dojo.load_people(file_name)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person (<person_id>) (<new_room_name>)"""
        person_id = arg['<person_id>']
        new_room = arg['<new_room_name>']
        self.dojo.reallocate_person(person_id, new_room)

    @docopt_cmd
    def do_display(self,arg):
        """ Usage: display"""
        self.dojo.display()

    @docopt_cmd
    def do_view_ids(self,arg):
        """Usage: view_ids"""
        self.dojo.view_person_id()

    def do_quit(self, arg):
        """ Quits out of Interactive Mode."""
        print('See ya, around!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
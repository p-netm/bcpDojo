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
    Dojo save_state [--db=database]
    Dojo load_state <sqlite_database>
    Dojo modify_room [office | living_space] <room_name> (--r=new_room_name | -d | -D | -c | -C)
    Dojo modify_person <person_identifier> [--id=new_id ] [ --first_name=new_name ] [ --second_name=new_name ] [ -d]
    Dojo promote_person <person_identifier>
    Dojo search_id_for <any_name> [<other_name>]
    Dojo display
    Dojo view_ids
    Dojo (-i | --interactive)
    Dojo (-h | --help | --version)

Options:
    create_room  takes in type of room and several rooms
    print_room  shows the people inside a room
    print_allocation  shows all people who have been allocated to any and all rooms
    add_person  adds a new fellow or staff
    modify_room  you can change any attribute of any room
    --r=new_room_name  rename the given room to a new room name
    -d  delete
    -D  same as -d but also reallocates people to any other available room
    -c  clears a room's occupants
    -C  empty the room as -c and also reassigns occupants to new rooms
    modify_person  change any property of stored data in regard to the given person
    --id=new_id  assign a new id
    --first_name=new_name  assign a new name to the first_name
    --second_name=new_name  assign a new second name
    promote_person  unidirectional upgrade from fellow to staff, never vice versa
    search_id  prints to console a lists of full names and their associative ids
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from program.dojo import Dojo


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
        if arg['fellow']:
            occupation = "fellow"
            accommodate = 'n'
            if arg['yes'] or arg['y']:
                accommodate = "yes"
            elif arg['no'] or arg['n']:
                accommodate = "no"
            self.dojo.add_person(arg['<first_name>'], arg['<second_name>'], occupation, accommodate)

        if arg['staff']:
            occupation = "staff".lower()
            self.dojo.add_person(arg['<first_name>'], arg['<second_name>'], occupation)

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
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database] """
        # print(arg){'--db': '.state.sqlite'}
        db_file = arg['--db']
        self.dojo.save_state(db_file)

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>  """
        db_file = arg['<sqlite_database>']
        self.dojo.load_state(db_file)

    @docopt_cmd
    def do_modify_room(self, arg):
        """Usage: modify_room [office | living_space] <room_name> (--r=new_room_name | -d | -D | -c | -C) """
        room_name = arg['<room_name>']
        new_room_name = arg['--r']
        room_type = False
        if arg['office']:
            room_type = "office"
        elif arg['living_space']:
            room_type = "living_space"
        d, D, c , C = arg['-d'], arg['-D'], arg['-c'], arg['-C']
        # modify_room(self, room_name, room_type=False, new_name=False, d=False, D=False, c=False, C=False)
        self.dojo.modify_room(room_name=room_name, room_type=room_type, new_name=new_room_name, d=d, D=D, c=c, C=C)

    @docopt_cmd
    def do_modify_person(self, arg):
        """Usage: modify_person <person_identifier> [--id=new_id ][ --first_name=new_name ][ --second_name=new_name ][ -d]"""
        person_id = arg['<person_identifier>']
        self.dojo.modify_person(id=person_id, new_id=arg['--id'], f_name=arg['--first_name'],
                                s_name=arg['--second_name'], delete=arg['-d'])
        print(arg)

    @docopt_cmd
    def do_search_id_for(self, arg):
        """Usage: search_id <any_name> [<other_name>] """
        if arg['<any_name>']:
            self.dojo.search_id_for(arg['<any_name>'], arg['<other_name>'])
        else:
            print("searching an id needs at least one name")

    @docopt_cmd
    def do_promote_person(self, arg):
        """Usage: promote_person <person_identifier> """
        print(arg)

    @docopt_cmd
    def do_display(self, arg):
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
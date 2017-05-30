# bcpDojo
A randomisation app that manages a housing facility

# BootcampProject
 a randomisation app that asigns housing facilities to occupants of the DOJO

 ## Introduction
 Dojo room Allocator add_people and randomly adds them to room that it selects from available rooms if there are any
 
 ## Problem Satatement
 
 When a new Fellow joins Andela they are assigned an office space and an optional living space if
they choose to opt in. When a new Staff joins they are assigned an office space only. In this
exercise you will be required to digitize and randomize a room allocation system for one of
Andela Kenya’s facilities called The Dojo.

## Constraints:

The Dojo has rooms, which can be offices or living spaces. An office can accommodate a
maximum of 6 people. A living space can accommodate a maximum of 4 people.
A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces.
Fellows have a choice to choose a living space or not.
This system will be used to automatically allocate spaces to people at random.

 ### features:
  #### create_room:
     Usage: create_room (living_space| office) <room_name>

  #### add_person:
     Usage: add_person <first_name> <second_name> (fellow [[yes|y]|[no|n]]|staff)
  
  #### print_room:
     Usage: print_room <room_name>
     Prints the names of all occupants within the provided room_name
     
  #### print_allocations:
     Usage: print_allocations [<file_name>]
     goes through all the rooms in the system and prints out the members of each room.
     if the file name argument is provided then the system also adds the names to the given file_name
     
  #### load_people:
     Usage: load_people (<file_name>)
     takes a preformatted text file, reads it, extracts the names of people inside the given filename and
     assigns each to a room
     

  ### Miscellaneous
  Meaning not part of the requirements.
  
  #### display:
    Usage: display
    prints out the current state of the system. prints out a graphical representation of the state of the system, 
    how and where a certain person name is or where a certain person object is stored as well as lists of 
    room name of al the rooms yet created
  
  #### view_ids:
    Usage:
    to reallocate a person you might need their ids; in a case where such is not given then, the admin can use this 
    function and print out all people added to the dojo as well as the ids that they gave when being registered 
    into the system.
    
 #### Extras:
  > -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.

## Demo

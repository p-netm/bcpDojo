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

 #### Extras:
  > -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.

## Demo

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class Person(base):
    __tablename__ = "persons"

    person_id = Column(String(10), primary_key=True)
    full_name = Column(String(100))
    occupation = Column(Enum('Fellow', 'Staff'))  # check and see if this can be translated to enum type ORMS
    office_name = Column(String, ForeignKey('rooms.room_name'), nullable=True)
    space_name = Column(String, ForeignKey('rooms.room_name'), nullable=True)

    person1 = relationship('Room', back_populates='persons')
    person2 = relationship('Room', back_populates='persons')

    def __init__(self, person_id, full_name, occ, office_name='None', space_name= "None"):
        self.person_id = person_id
        self.full_name = full_name
        self.occupation = occ
        self.office_name = office_name
        self.space_name = space_name


class Room(base):
    __tablename__ = "rooms"

    room_name = Column(String, primary_key=True)
    room_type = Column(Enum('office', 'living_space'), nullable=False)
    occupants = Column(Integer, nullable=False)



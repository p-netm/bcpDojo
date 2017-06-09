from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class Person(base):
    __tablename__ = "Persons"

    person_id = Column(String, primary_key=True)
    full_name = Column(String)
    occupation = Column(String)  # check and see if this can be translated to enum type ORMS
    office_name = Column(String, ForeignKey('Offices.office_name'), nullable=True)
    living_space_name = Column(String, ForeignKey('Living_spaces.living_space_name'), nullable=True)

    def __init__(self, id, f_name, occupation, office="None", space="None"):
        self.person_id = id
        self.full_name = f_name
        self.occupation = occupation
        self.office_name = office
        self.living_space_name = space


class Office(base):
    __tablename__ = "Offices"

    office_name = Column(String, primary_key=True)

    def __init__(self, office_name):
        self.office_name = office_name


class Living_space(base):
    __tablename__ = "Living_spaces"

    living_space_name = Column(String, primary_key=True)

    def __init__(self, space_name):
        self.living_space_name = space_name




def retrieve_office_rooms():
    session.query(Office).all()


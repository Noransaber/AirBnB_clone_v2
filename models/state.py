#!/usr/bin/python3
""" STATE MODULE """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from base_model import Base, BaseModel
from city import City


class State(BaseModel, Base):
    """ CLASS STATE """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete')

    @property
    def associated_cities(self):
        """ Returns a list of cities associated with this state """
        cities_instances = []
        for city in models.storage.all(models.City).values():
            if city.state_id == self.id:
                cities_instances.append(city)
        return cities_instances

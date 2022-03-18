import time
import math
import random
import configparser
import asyncio

config = configparser.ConfigParser()
config.read("config")

TIME_UNIT = float(config['PARAMS']['time_unit'])


class RawMaterial:

    """Parent class of materials with a serial number"""

    @classmethod
    def incr(cls):
        "Ensures materials all have different serial numbers"
        cls.serial_count += 1
        return cls.serial_count

    def __init__(self):
        self.serial_number = self.incr()

    @property
    def material_type(self):
        "Retuns the type of material"
        return self.__class__.__name__.lower()

    def get_id(self):
        "Retuns the id of material"
        return self.serial_number

    def __repr__(self):
        return f"{self.material_type} number {self.get_id()}"

class Foo(RawMaterial):
    "Foo"
    serial_count = 0

class Bar(RawMaterial):
    "Bar"
    serial_count = 0

class Foobar(RawMaterial):
    "Foobar"
    def __init__(self, foo, bar):
        self.serial_number = f"{foo.get_id()}-{bar.get_id()}"

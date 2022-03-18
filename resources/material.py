import time
import math
import random
import configparser
import asyncio
from resources.tools import verboseprint

config = configparser.ConfigParser()
config.read("config")

TIME_UNIT = float(config['PARAMS']['time_unit'])


class RawMaterial:
    """Parent class of materials with a serial number"""

    @classmethod
    def incr(cls):
        cls.serial_count += 1
        return cls.serial_count

    def __init__(self):
        self.serial_number = self.incr()

    @property
    def material_type(self):
        return self.__class__.__name__.lower()

    def get_id(self):
        return self.serial_number

    def __repr__(self):
        return f"{self.material_type} number {self.get_id()}"

class Foo(RawMaterial):
    serial_count = 0

class Bar(RawMaterial):
    serial_count = 0

class Foobar(RawMaterial):
    def __init__(self, foo, bar):
        self.serial_number = str(foo.get_id()) + str(bar.get_id())

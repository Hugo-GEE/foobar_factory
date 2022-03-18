"""Contains composite class implementation of factory
and two of its components : warehouse and wallet"""

from __future__ import annotations
import time
import asyncio
from resources.robots import Robot
from resources.tools import TIME_UNIT


class FoobarFactory:

    """Represents our factory, with robots, production line and warehouse"""

    def __init__(self):
        self.warehouse = Warehouse()
        self.robots = []
        self.wallet = Wallet()
        self.clock = 0
        self.round_counter = 0
        self.start_time = time.time()
        self.start_cpu_time = time.process_time()

    async def time(self, duration:int):
        "Allows to count the cumulated time of robots activity"
        await asyncio.sleep(duration*TIME_UNIT)
        self.clock += duration

    def add_robot(self):
        "Adds a robot to the factory"
        self.robots.append(Robot(self))

    async def take_over_foobar_market(self, robot:Robot):
        "Determines and performs the actions required to buy a robot or buys a robot"
        take_over_code = await robot.buy_robot(self.warehouse, self.wallet)
        if take_over_code == "need foo":
            await robot.mine('foo', self.warehouse)
        elif take_over_code == "need cash":
            sale_code = await robot.sell_foobar(self.warehouse, self.wallet)
            if sale_code == "need foobar":
                await robot.produce_foobars(self.warehouse)
        else:
            self.add_robot()

class Warehouse:

    """Stores raw materials and finished products"""

    def __init__(self):
        self._warehouse = {'foo':[], 'bar':[], 'foobar':[]}

    def get(self, material_type:str) -> int:
        "Returns amount of given material"
        return len(self._warehouse[material_type])

    def take(self, material_type:str, amount:int=1) -> RawMaterial:
        "Hands over material from warehouse"
        if self.get(material_type)<amount:
            exception_message = f"{self.get(material_type)} {material_type} in warehouse, cannot take {amount}"
            raise Exception(exception_message)
        return self._warehouse[material_type].pop()

    def store(self, raw_material:RawMaterial):
        "Stores given material from warehouse"
        self._warehouse[raw_material.material_type].append(raw_material)


class Wallet:

    "Stores cash"

    def __init__(self):
        self._wallet = 0

    def set(self, amount:int):
        "Adds or substracts given amount of cash"
        self._wallet += amount

    def get(self) -> int:
        "Returns amount of cash"
        return self._wallet

    def __repr__(self) -> str:
        return f"€{self._wallet}"

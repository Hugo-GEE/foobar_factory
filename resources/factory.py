import time
import math
import random
import configparser
import asyncio
from resources.robots import Robot
from resources.tools import verboseprint

config = configparser.ConfigParser()
config.read("config")

TIME_UNIT = float(config['PARAMS']['time_unit'])

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

    async def time(self, duration):
        await asyncio.sleep(duration*TIME_UNIT)
        self.clock += duration

    def add_robot(self):
        self.robots.append(Robot(self))

    async def take_over_foobar_market(self, robot):
        self.round_counter += 1
        verboseprint('vv', self.report())
        take_over_code = await robot.buy_robot(self.warehouse, self.wallet)
        if take_over_code == "need foo":
            await robot.mine('foo', self.warehouse)
        elif take_over_code == "need cash":
            sale_code = await robot.sell_foobar(self.warehouse, self.wallet)
            if sale_code == "need foobar":
                await robot.produce_foobars(self.warehouse)
        else:
            self.add_robot()

    def report(self, final:bool=False, json:bool=False):
        round_counter = f"round {self.round_counter}"
        foobars = f"{self.warehouse.get('foobar')} foobars"
        foo = f"{self.warehouse.get('foo')} foo"
        cum_factory_time =  f"Cumulated factory time {round(self.clock/60, 1)}min"
        cash = f"€{self.wallet}"
        robots = f"{len(self.robots)} robots"
        parameters = [round_counter, cum_factory_time, foobars, foo, cash, robots]
        if final is True:
            real_time = f"Real time = {round(time.time() - self.start_time, int(-math.log(TIME_UNIT)/3))}s"
            cpu_time = f"Process time = {round(time.process_time() - self.start_cpu_time, int(-math.log(TIME_UNIT)/3))}s"
            cum_time =  f"Cumulated real time = {round(self.clock*TIME_UNIT, int(-math.log(TIME_UNIT)/3))}s"
            parameters.remove(foobars)
            parameters.remove(cash)
            parameters.remove(cum_factory_time)
            parameters.remove(robots)
            parameters += [real_time, cpu_time, cum_time]
        if json is True:
            return parameters
        return '\n\t' + " | ".join(parameters) + "\n"


class Warehouse:
    """Stores raw materials and finished products"""
    def __init__(self):
        self._warehouse = {'foo':[], 'bar':[], 'foobar':[]}

    def get(self, material_type):
        return len(self._warehouse[material_type])

    def take(self, material_type, amount=1):
        if self.get(material_type)<amount:
            exception_message = f"{self.get(material_type)} {material_type} in warehouse, cannot take {amount}"
            raise Exception(exception_message)
        return self._warehouse[material_type].pop()

    def store(self, raw_material):
        self._warehouse[raw_material.material_type].append(raw_material)


class Wallet:

    def __init__(self):
        self._wallet = 0

    def set(self, amount):
        self._wallet += amount

    def get(self):
        return self._wallet

    def __repr__(self):
        return f"€{self._wallet}"

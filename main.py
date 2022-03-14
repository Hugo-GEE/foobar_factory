import time
import math
import random
import configparser
import asyncio


config = configparser.ConfigParser()
config.read("config")

TIME_UNIT = float(config['PARAMS']['time_unit'])
ROBOT_NAMES = config['ROBOT_NAMES']['robot_names'].split(',')
random.shuffle(ROBOT_NAMES)
ROBOT_OFFSET = len(ROBOT_NAMES)
VERBOSE = 'v'

def verboseprint(verbose_level, *args):
    if VERBOSE == 'vvv':
        print(*args)
    if VERBOSE == 'vv':
        if verbose_level == 'vv' or verbose_level == 'v':
            print(*args)
    if VERBOSE == 'v':
        if verbose_level == 'v':
            print(*args)


async def main(robots_to_finish = 30):
    """Instantiate Robots and produce foobars"""
    foobar_factory = FoobarFactory()
    foobar_factory.add_robot()
    foobar_factory.add_robot()
    while len(foobar_factory.robots) < robots_to_finish:
        await asyncio.gather(
                            *[foobar_factory.take_over_foobar_market(robot)
                            for robot in foobar_factory.robots])

    verboseprint('v', foobar_factory.report(final=True))
    verboseprint('v', "\nFoobar market domination achieved. Next, world.\n")



class FoobarFactory:
    """Represents our factory, with robots, production line and warehouse"""

    def __init__(self):
        self.warehouse = Warehouse()
        self.robots = []
        self.wallet = 0
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
        take_over_code = await robot.buy_robot()
        if take_over_code == "need foo":
            await robot.mine_foo()
        elif take_over_code == "need cash":
            sale_code = await robot.sell_foobar()
            if sale_code == "need foobar":
                await robot.produce_foobars()
        else:
            self.add_robot()

    def report(self, final=False):
        round_counter = f"round {self.round_counter}"
        foobars = f"{self.warehouse.get('foobar')} foobars"
        cum_factory_time =  f"Cumulated factory time {round(self.clock/60, 1)}min"
        cash = f"€{self.wallet}"
        robots = f"{len(self.robots)} robots"
        parameters = [round_counter, cum_factory_time, foobars, cash, robots]
        if final:
            real_time = f"Real time = {round(time.time() - self.start_time, int(-math.log(TIME_UNIT)/3))}s"
            cpu_time = f"Process time = {round(time.process_time() - self.start_cpu_time, int(-math.log(TIME_UNIT)/3))}s"
            cum_time =  f"Cumulated real time {round(self.clock*TIME_UNIT, int(-math.log(TIME_UNIT)/3))}s"
            parameters.remove(foobars)
            parameters.remove(cash)
            parameters.remove(cum_factory_time)
            parameters.remove(robots)
            parameters += [real_time, cpu_time, cum_time]
        return '\n\t' + " | ".join(parameters) + "\n"


class Robot:

    """Foobar production robot """

    robot_offest = ROBOT_OFFSET

    @classmethod
    def incr(self):
        if len(ROBOT_NAMES) >= 1:
            return ROBOT_NAMES.pop()
        else:
            self.robot_offest += 1
            return f"robot_{self.robot_offest }"

    def __init__(self, parent):
        self.name = self.incr()
        self.warehouse = parent.warehouse
        self.wallet = parent.wallet
        self.time = parent.time
        self.activity = None

    async def manage_activity(self, activity):
        if self.activity != activity:
            verboseprint('vvv', f"[{self.name}] changing from {self.activity} to {activity}")
            await self.time(5)
            self.activity = activity

    async def produce_foobars(self):
        producton_code = await self.assemble_foobar()
        if producton_code == 'need foo':
            await self.mine_foo()
        elif producton_code == 'need bar':
            await self.mine_bar()

    async def mine_foo(self):
        """occupies the robot for 1 second"""

        await self.manage_activity("mining foo")
        verboseprint('vv', f"[{self.name}] Mining foo\n")
        await self.time(1)
        result = self.warehouse.store((mined_foo := Foo()))
        verboseprint('vvv', f"[{self.name}] Mined {mined_foo}\n")

        return result

    async def mine_bar(self):
        """keeps the robot busy for a random time between 0.5 and 2 seconds"""

        await self.manage_activity("mining bar")
        verboseprint('vv', f"[{self.name}] Mining bar\n")
        await self.time(random.uniform(0.5, 2))
        result = self.warehouse.store((mined_bar := Bar()))
        verboseprint('vvv', f"[{self.name}] Mined {mined_bar}\n")
        return result

    async def assemble_foobar(self):
        """Assembling a foobar from a foo and a bar: keeps the robot busy for 2 seconds.
        The operation has a 60% chance of success; in case of failure the bar can be reused, the foo is lost"""

        verboseprint('vv', f"[{self.name}] Trying to assemble foobar")
        if self.warehouse.get('foo') < 1:
            verboseprint('vv', f"[{self.name}] Not enough foo to assemble")
            return 'need foo'

        if self.warehouse.get('bar') < 1:
            verboseprint('vv', f"[{self.name}] Not enough bar to assemble")
            return 'need bar'

        foo = self.warehouse.take('foo')
        bar = self.warehouse.take('bar')
        await self.manage_activity("assembling foobar")
        await self.time(2)
        if random.randint(1, 10) <= 6:
            verboseprint('vv', f"[{self.name}] Assembly successful")
            self.warehouse.store((foobar := Foobar(foo, bar)))
            verboseprint('vv', f"[{self.name}] {foobar} is being stored\n")
            return 0
        else:
            verboseprint('vv', f"[{self.name}] Assembly failed\n")
            self.warehouse.store(bar)
            return 1


    async def sell_foobar(self):
        """Sell foobar: 10s to sell from 1 to 5 foobar, we earn €1 per foobar sold"""

        verboseprint('vv', f"[{self.name}] Selling foobar")
        if self.warehouse.get('foobar') < 5:
            verboseprint('vv', f"[{self.name}] Not enough foobar to sell")
            return 'need foobar'

        foobar_market = []
        while self.warehouse.get('foobar') >= 1 and len(foobar_market) <= 5:
            foobar_market.append(self.warehouse.take('foobar'))
        await self.manage_activity("selling foobar")
        await self.time(10)
        foobar_batch = len(foobar_market)
        self.wallet += foobar_batch
        foobar_market.clear()
        verboseprint('vv', f"[{self.name}] Sold {foobar_batch} foobar(s)\n")
        return 0

    async def buy_robot(self):
        verboseprint('vv', f"[{self.name}] Trying to buy robot")
        if self.warehouse.get('foo') < 6:
            verboseprint('vv', f"[{self.name}] Not enough foo to buy robot")
            return 'need foo'

        if self.wallet < 3:
            verboseprint('vv', f"[{self.name}] Not enough cash to buy robot\n")
            return 'need cash'

        verboseprint('vv', f"[{self.name}] Buying robot\n")
        self.warehouse.take('foo', 6)
        await self.manage_activity("buying robot")
        self.wallet -= 3
        return 0


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


class RawMaterial:
    """Parent class of materials with a serial number"""

    @classmethod
    def incr(self):
        self.serial_count += 1
        return self.serial_count

    def __init__(self):
        self.serial_number = self.incr()
        self.material_type = self.__class__.__name__.lower()

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
        self.material_type = self.__class__.__name__.lower()


if __name__ == "__main__":
    asyncio.run(main(30))

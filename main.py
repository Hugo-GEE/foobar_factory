import time
import random
import configparser
import asyncio



config = configparser.ConfigParser()
config.read("config")

TIME_UNIT = float(config['PARAMS']['time_unit'])
ROBOT_NAMES = config['ROBOT_NAMES']['robot_names'].split(',')
ROBOT_OFFSET = len(ROBOT_NAMES)



async def main():
    """Instantiate Robots and produce foobars"""
    foobar_factory = FoobarFactory()
    foobar_factory.add_robot()
    foobar_factory.add_robot()
    while len(foobar_factory.robots) < 30:
        await asyncio.gather(
                            *[foobar_factory.take_over_foobar_market(robot)
                            for robot in foobar_factory.robots])

    print("Foobar market domination achieved. Next, world.")



class FoobarFactory:
    """Represents our factory, with robots, production line and warehouse"""

    def __init__(self):
        self.warehouse = Warehouse()
        self.robots = []
        self.wallet = 0
        self.clock = 0

    async def time(self, duration):
        await asyncio.sleep(duration*TIME_UNIT)
        self.clock += duration

    def add_robot(self):
        self.robots.append(Robot(self))

    async def take_over_foobar_market(self, robot):
        round_counter = 0
        print(f"""round {round_counter} |
                  time = {round(self.clock/60, 1)} min |
                  {self.warehouse.get_foobar()} foobars |
                  €{self.wallet} |
                  {len(self.robots)} robots""")
        round_counter += 1
        take_over_code = robot.buy_robot()
        if take_over_code == "need foo":
            await robot.mine_foo()
        elif take_over_code == "need cash":
            sale_code = await robot.sell_foobar()
            if sale_code == "need foobar":
                await robot.produce_foobars()
        else:
            self.add_robot()


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

    async def mine_foo(self):
        """occupies the robot for 1 second"""
        print(f"[{self.name}] Mining foo\n")
        await self.time(1)
        result = self.warehouse.store('foo')
        return result

    async def mine_bar(self):
        """keeps the robot busy for a random time between 0.5 and 2 seconds"""
        print(f"[{self.name}] Mining bar\n")
        await self.time(random.uniform(0.5, 2))
        result = self.warehouse.store('bar')
        return result

    async def assemble_foobar(self):
        """Assembling a foobar from a foo and a bar: keeps the robot busy for 2 seconds.
        The operation has a 60% chance of success; in case of failure the bar can be reused, the foo is lost"""

        print(f"[{self.name}] Trying to assemble foobar")
        if self.warehouse.get('foo') < 1:
            print(f"[{self.name}] Not enough foo to assemble")
            return 'need foo'

        if self.warehouse.get('bar') < 1:
            print(f"{self.name} Not enough bar to assemble")
            return 'need bar'

        self.warehouse.take('foo')
        self.warehouse.take('bar')
        await self.time(2)
        if random.randint(1, 10) <= 6:
            print("Assembly successful")
            foobar = Foobar()
            print(f"[{self.name}] {foobar} is being stored\n")
            self.warehouse.store_foobar(foobar)
            return 0
        else:
            print(f"[{self.name}] Assembly failed\n")
            self.warehouse.store('bar')
            return 1

    async def produce_foobars(self):
        producton_code = await self.assemble_foobar()
        if producton_code == 'need foo':
            await self.mine_foo()
        elif producton_code == 'need bar':
            await self.mine_bar()


    async def sell_foobar(self):
        """Sell foobar: 10s to sell from 1 to 5 foobar, we earn €1 per foobar sold"""

        print("Selling foobar")
        if self.warehouse.get_foobar() < 4:
            print(f"{self.name} Not enough foobar to sell")
            return 'need foobar'

        foobar_market = []
        while self.warehouse.get_foobar() >= 1 and len(foobar_market) <= 5:
            foobar_market.append(self.warehouse.take_foobar())
        await self.time(10)
        foobar_batch = len(foobar_market)
        self.wallet += foobar_batch
        foobar_market.clear()
        print(f"[{self.name}] Sold {foobar_batch} foobar(s)\n")
        return 0

    def buy_robot(self):
        print("Trying to buy robot")
        if self.warehouse.get('foo') < 6:
            print(f"[{self.name}] Not enough foo to buy robot")
            return 'need foo'

        if self.wallet < 3:
            print(f"[{self.name}] Not enough cash to buy robot\n")
            return 'need cash'

        print(f"[{self.name}] Buying robot\n")
        self.warehouse.take('foo', 6)
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
            raise Exception(f"{self.get(material_type)} {material_type} in warehouse, cannot take {amount}")
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

import time
import random
import configparser



config = configparser.ConfigParser()
config.read("config")

TIME_UNIT = float(config['PARAMS']['time_unit'])


def main():
    """Instantiate Robots and produce foobars"""
    my_factory = FoobarFactory()
    my_factory.add_robot()

    my_factory.take_over_foobar_market()


class FoobarFactory:
    """Represents our factory, with robots, production line and warehouse"""

    def __init__(self):
        self.warehouse = Warehouse()
        self.robots = []
        self.wallet = 0

    def add_robot(self):
        self.robots.append(Robot(self))

    def take_over_foobar_market(self):
        round_counter = 0
        while len(self.robots) < 30:
            print(f"round {round_counter} | {self.warehouse.get_foobar()} foobars | €{self.wallet} | {len(self.robots)} robots")
            round_counter += 1
            take_over_code = self.robots[0].buy_robot()
            if take_over_code == "need foo":
                self.robots[0].mine_foo()
            elif take_over_code == "need cash":
                sale_code = self.robots[0].sell_foobar()
                if sale_code == 'need foobar':
                    self.produce_foobars()
            else:
                self.robots.append(Robot(self))
        print("Foobar market domination achieved. Next, world.")

    def produce_foobars(self):
        producton_code = self.robots[0].assemble_foobar()
        if producton_code == 'need foo':
            self.robots[0].mine_foo()
        elif producton_code == 'need bar':
            self.robots[0].mine_bar()


class Robot:

    """Foobar production robot """

    def __init__(self, parent):
        self.warehouse = parent.warehouse
        self.wallet = parent.wallet

    def mine_foo(self):
        """occupies the robot for 1 second"""
        print("Mining foo\n")
        time.sleep(TIME_UNIT)
        result = self.warehouse.store('foo')
        return result

    def mine_bar(self):
        """keeps the robot busy for a random time between 0.5 and 2 seconds"""
        print("Mining bar\n")
        time.sleep(random.uniform(0.5*TIME_UNIT, 2*TIME_UNIT))
        result = self.warehouse.store('bar')
        return result

    def assemble_foobar(self):
        """Assembling a foobar from a foo and a bar: keeps the robot busy for 2 seconds.
        The operation has a 60% chance of success; in case of failure the bar can be reused, the foo is lost"""

        print("Trying to assemble foobar")
        if self.warehouse.get('foo') < 1:
            print('Not enough foo to assemble')
            return 'need foo'

        if self.warehouse.get('bar') < 1:
            print('Not enough bar to assemble')
            return 'need bar'

        self.warehouse.take('foo')
        self.warehouse.take('bar')
        time.sleep(2*TIME_UNIT)
        if random.randint(1, 10) <= 6:
            print("Assembly successful")
            foobar = Foobar()
            print(f"{foobar} is being stored\n")
            self.warehouse.store_foobar(foobar)
            return 0
        else:
            print("Assembly failed\n")
            self.warehouse.store('bar')
            return 1

    def sell_foobar(self):
        """Sell foobar: 10s to sell from 1 to 5 foobar, we earn €1 per foobar sold"""

        print("Selling foobar")
        if self.warehouse.get_foobar() < 4:
            print('Not enough foobar to sell')
            return 'need foobar'

        foobar_market = []
        while self.warehouse.get_foobar() >= 1 and len(foobar_market) <= 5:
            foobar_market.append(self.warehouse.take_foobar())
        time.sleep(10*TIME_UNIT)
        foobar_batch = len(foobar_market)
        self.wallet += foobar_batch
        foobar_market.clear()
        print(f"Sold {foobar_batch} foobar(s)\n")
        return 0

    def buy_robot(self):
        print("Trying to buy robot")
        if self.warehouse.get('foo') < 6:
            print('Not enough foo to buy robot')
            return 'need foo'

        if self.wallet < 3:
            print('Not enough cash to buy robot\n')
            return 'need cash'

        print("Buying robot\n")
        self.warehouse.take('foo', 6)
        self.wallet -= 3
        return 0


class Warehouse:
    """Stores raw materials and finished products"""
    def __init__(self):
        self._warehouse = {'foo':0, 'bar':0, 'foobar':[]}

    def get(self, raw_material):
        return self._warehouse[raw_material]

    def get_foobar(self):
        return len(self._warehouse['foobar'])

    def take(self, raw_material, amount=1):
        if self._warehouse[raw_material]<amount:
            raise Exception(f"{self._warehouse[raw_material]} {raw_material} in warehouse, cannot take {amount}")
        self._warehouse[raw_material] -= 1
        return 0

    def store(self, raw_material):
        self._warehouse[raw_material] += 1
        return 0

    def store_foobar(self, foobar):
        self._warehouse['foobar'].append(foobar)

    def take_foobar(self):
        if len(self._warehouse['foobar']) < 1:
            raise Exception(f"No foobar in warehouse, cannot take!")
        return self._warehouse['foobar'].pop()

class Foobar:
    """Foobar objects with a serial number"""

    #Alternative implemetation
    """import itertools
    id_iter = itertools.count()
    def __init__(self):
        self.id = next(BarFoo.id_iter)"""

    serial_count = 0

    @classmethod
    def incr(self):
        self.serial_count += 1
        return self.serial_count

    def __init__(self):
        self.serial_number = self.incr()

    def get_id(self):
        return self.serial_number

    def __repr__(self):
        return f"Foobar number {self.get_id()}"



if __name__ == "__main__":
    main()

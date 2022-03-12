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

    my_factory.launch_production()


class FoobarFactory:
    """Represents our factory, with robots, production line and warehouse"""

    def __init__(self):
        self.warehouse = Warehouse()
        self.robot = None

    def add_robot(self):
        self.robot = Robot(self)

    def launch_production(self):
        while True:
            print(f"{self.warehouse.get_foobar()} foobars in the warehouse")
            producton_code = self.robot.assemble_foobar()
            if producton_code == 0:
                pass
            elif producton_code == 1:
                pass
            elif producton_code == 'need foo':
                self.robot.mine_foo()
            elif producton_code == 'need bar':
                self.robot.mine_bar()


class Robot:

    """Foobar production robot """

    def __init__(self, parent):
        self.warehouse = parent.warehouse

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

        print("Assembling foobar")
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


class Warehouse:
    """Stores raw materials and finished products"""
    def __init__(self):
        self._warehouse = {'foo':0, 'bar':0, 'foobar':{}}

    def get(self, raw_material):
        return self._warehouse[raw_material]

    def get_foobar(self):
        return len(self._warehouse['foobar'])

    def take(self, raw_material):
        if self._warehouse[raw_material]<1:
            print(f"No {raw_material} in warehouse")
            if raw_material == 'foo':
                return 2
            if raw_material == 'bar':
                return 3
        self._warehouse[raw_material] -= 1
        return 0

    def store(self, raw_material):
        self._warehouse[raw_material] += 1
        return 0

    def store_foobar(self, foobar):
        self._warehouse['foobar'][foobar.get_id()] = foobar

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

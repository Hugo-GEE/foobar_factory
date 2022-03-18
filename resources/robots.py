import time
import math
import random
import configparser
import asyncio
from resources.tools import verboseprint
from resources.material import *


config = configparser.ConfigParser()
config.read("config")

ROBOT_NAMES = config['ROBOT_NAMES']['robot_names'].split(',')
random.shuffle(ROBOT_NAMES)
ROBOT_OFFSET = len(ROBOT_NAMES)

class Robot:

    """Foobar production robot """

    robot_offest = ROBOT_OFFSET

    @classmethod
    def incr(self):
        if len(ROBOT_NAMES) >= 1:
            return ROBOT_NAMES.pop()
        else:
            self.robot_offest += 1
            return f"robot_{self.robot_offest}"

    def __init__(self, parent):
        self.name = self.incr()
        self.time = parent.time
        self.activity = None

    async def manage_activity(self, activity):
        if self.activity is not None and self.activity != activity:
            verboseprint('vvv', f"[{self.name}] changing from {self.activity} to {activity}")
            await self.time(5)
            self.activity = activity

    async def produce_foobars(self, warehouse):
        producton_code = await self.assemble_foobar(warehouse)
        if producton_code == 'need foo':
            await self.mine('foo', warehouse)
        elif producton_code == 'need bar':
            await self.mine('bar', warehouse)

    async def mine(self, material_type, warehouse):
        """occupies the robot for 1 second"""
        if material_type == 'foo':
            await self.manage_activity("mining foo")
            verboseprint('vv', f"[{self.name}] Mining foo\n")
            await self.time(1)
            result = warehouse.store((mined_foo := Foo()))
            verboseprint('vvv', f"[{self.name}] Mined {mined_foo}\n")
        if material_type == 'bar':
            await self.manage_activity("mining bar")
            verboseprint('vv', f"[{self.name}] Mining bar\n")
            await self.time(random.uniform(0.5, 2))
            result = warehouse.store((mined_bar := Bar()))
            verboseprint('vvv', f"[{self.name}] Mined {mined_bar}\n")

    async def assemble_foobar(self, warehouse):
        """Assembling a foobar from a foo and a bar: keeps the robot busy for 2 seconds.
        The operation has a 60% chance of success; in case of failure the bar can be reused, the foo is lost"""

        verboseprint('vv', f"[{self.name}] Trying to assemble foobar")
        if warehouse.get('foo') < 1:
            verboseprint('vv', f"[{self.name}] Not enough foo to assemble")
            return 'need foo'

        if warehouse.get('bar') < 1:
            verboseprint('vv', f"[{self.name}] Not enough bar to assemble")
            return 'need bar'

        foo = warehouse.take('foo')
        bar = warehouse.take('bar')
        await self.manage_activity("assembling foobar")
        await self.time(2)
        if random.randint(1, 10) <= 6:
            verboseprint('vv', f"[{self.name}] Assembly successful")
            warehouse.store((foobar := Foobar(foo, bar)))
            verboseprint('vv', f"[{self.name}] {foobar} is being stored\n")
            return 0
        else:
            verboseprint('vv', f"[{self.name}] Assembly failed\n")
            warehouse.store(bar)
            return 1

    async def sell_foobar(self, warehouse, wallet):
        """Sell foobar: 10s to sell from 1 to 5 foobar, we earn €1 per foobar sold"""

        verboseprint('vv', f"[{self.name}] Selling foobar")
        if warehouse.get('foobar') < 5:
            verboseprint('vv', f"[{self.name}] Not enough foobar to sell")
            return 'need foobar'

        foobar_market = []
        while warehouse.get('foobar') >= 1 and len(foobar_market) <= 5:
            foobar_market.append(warehouse.take('foobar'))
        await self.manage_activity("selling foobar")
        await self.time(10)
        foobar_batch = len(foobar_market)
        wallet.set(foobar_batch)
        foobar_market.clear()
        verboseprint('vv', f"[{self.name}] Sold {foobar_batch} foobar(s)\n")

    async def buy_robot(self, warehouse, wallet):
        verboseprint('vv', f"[{self.name}] Trying to buy robot")
        if warehouse.get('foo') < 6:
            verboseprint('vv', f"[{self.name}] Not enough foo to buy robot")
            return 'need foo'

        if wallet.get() < 3:
            verboseprint('vv', f"[{self.name}] Not enough cash to buy robot\n")
            return 'need cash'

        verboseprint('vv', f"[{self.name}] Buying robot\n")
        warehouse.take('foo', 6)
        await self.manage_activity("buying robot")
        wallet.set(-3)

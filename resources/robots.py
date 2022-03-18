import time
import math
import asyncio
import logging
from typing import Optional
from resources.material import *
from resources.tools import *

random.seed(SEED)

class Robot:

    """Foobar production robot """

    robot_offest = ROBOT_OFFSET

    @classmethod
    def incr(self)->str:
        "Ensures each robot gets a different name"
        if len(ROBOT_NAMES) >= 1:
            return ROBOT_NAMES.pop()
        else:
            self.robot_offest += 1
            return f"robot_{self.robot_offest}"

    def __init__(self, parent:FoobarFactory):
        self.name = self.incr()
        self.time = parent.time
        self.activity = None

    async def manage_activity(self, activity):
        "Moving to change activity: occupies the robot for 5 seconds"
        if self.activity is not None and self.activity != activity:
            logging.debug(f"[{self.name}] changing from {self.activity} to {activity}")
            await self.time(5)
            self.activity = activity

    async def produce_foobars(self, warehouse):
        "Determines and performs the actions necessary to produce a foobar or produces a foobar"
        producton_code = await self.assemble_foobar(warehouse)
        if producton_code == 'need foo':
            await self.mine('foo', warehouse)
        elif producton_code == 'need bar':
            await self.mine('bar', warehouse)

    async def mine(self, material_type, warehouse):
        """Mine material. Occupies the robot for 1 second"""
        if material_type == 'foo':
            await self.manage_activity("mining foo")
            logging.debug(f"[{self.name}] Mining foo\n")
            await self.time(1)
            result = warehouse.store((mined_foo := Foo()))
            logging.debug(f"[{self.name}] Mined {mined_foo}\n")
        if material_type == 'bar':
            await self.manage_activity("mining bar")
            logging.debug(f"[{self.name}] Mining bar\n")
            await self.time(random.uniform(0.5, 2))
            result = warehouse.store((mined_bar := Bar()))
            logging.debug(f"[{self.name}] Mined {mined_bar}\n")

    async def assemble_foobar(self, warehouse):
        """Assembling a foobar from a foo and a bar: keeps robot busy for 2 seconds.
        60% chance of success; in case of failure, bar can be reused, foo is lost"""

        logging.debug(f"[{self.name}] Trying to assemble foobar")
        if warehouse.get('foo') < 1:
            logging.debug(f"[{self.name}] Not enough foo to assemble")
            return 'need foo'

        if warehouse.get('bar') < 1:
            logging.debug(f"[{self.name}] Not enough bar to assemble")
            return 'need bar'

        foo = warehouse.take('foo')
        bar = warehouse.take('bar')
        await self.manage_activity("assembling foobar")
        await self.time(2)
        if random.randint(1, 10) <= 6:
            logging.debug(f"[{self.name}] Assembly successful")
            warehouse.store((foobar := Foobar(foo, bar)))
            logging.debug(f"[{self.name}] {foobar} is being stored\n")
            return 0
        else:
            logging.debug(f"[{self.name}] Assembly failed\n")
            warehouse.store(bar)
            return 1

    async def sell_foobar(self, warehouse, wallet):
        """Sell foobar: 10s to sell from 1 to 5 foobar, we earn €1 per foobar sold"""

        logging.debug(f"[{self.name}] Selling foobar")
        if warehouse.get('foobar') < 5:
            logging.debug(f"[{self.name}] Not enough foobar to sell")
            return 'need foobar'

        foobar_market = []
        while warehouse.get('foobar') >= 1 and len(foobar_market) <= 5:
            foobar_market.append(warehouse.take('foobar'))
        await self.manage_activity("selling foobar")
        await self.time(10)
        foobar_batch = len(foobar_market)
        wallet.set(foobar_batch)
        foobar_market.clear()
        logging.debug(f"[{self.name}] Sold {foobar_batch} foobar(s)\n")

    async def buy_robot(self, warehouse, wallet):
        logging.debug(f"[{self.name}] Trying to buy robot")
        if warehouse.get('foo') < 6:
            logging.debug(f"[{self.name}] Not enough foo to buy robot")
            return 'need foo'

        if wallet.get() < 3:
            logging.debug(f"[{self.name}] Not enough cash to buy robot\n")
            return 'need cash'

        logging.debug(f"[{self.name}] Buying robot\n")
        warehouse.take('foo', 6)
        await self.manage_activity("buying robot")
        wallet.set(-3)

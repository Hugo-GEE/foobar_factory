import unittest
import json
from main import *
from io import StringIO


class TestFoobarFactory(unittest.IsolatedAsyncioTestCase):

    async def test_buy_robot(self):
        foobar_test_factory = FoobarFactory()
        foobar_test_factory.add_robot()
        for i in range(6):
            foobar_test_factory.robots[0].warehouse.store(Foo())
        foobar_test_factory.robots[0].wallet += 3
        verboseprint('v', foobar_test_factory.report())

        while len(foobar_test_factory.robots) < 2:
            await asyncio.gather(
                                *[foobar_test_factory.take_over_foobar_market(robot)
                                for robot in foobar_test_factory.robots])
        verboseprint('v', foobar_test_factory.report())

        self.assertEqual(2, len(foobar_test_factory.robots), "Robots were not bought when resources available")

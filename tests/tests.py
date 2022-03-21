"Tests"

import unittest
import json
import pdb
import os
from main import main
from resources.material import Foo, Bar, Foobar
from resources.tools import report
from resources.factory import FoobarFactory


class TestFoobarFactory(unittest.IsolatedAsyncioTestCase):

    async def test_take_empty_material_market(self):
        foobar_test_factory = FoobarFactory()
        with self.assertRaises(Exception) as exc:
            foobar_test_factory.warehouse.take('foo')
        self.assertEqual(str(exc.exception), "0 foo in warehouse, cannot take 1")

    async def test_buy_robot(self):
        foobar_test_factory = FoobarFactory(number_of_robots=1)
        for _ in range(6):
            foobar_test_factory.warehouse.store(Foo())
        foobar_test_factory.wallet.set(3)
        await foobar_test_factory.take_over_foobar_market(foobar_test_factory.robots[0])
        self.assertEqual(2, len(foobar_test_factory.robots), "Robots were not bought when resources available")

    async def test_assemble_foobar(self):
        foobar_test_factory = FoobarFactory(number_of_robots=1)
        for _ in range(7):
            foobar_test_factory.warehouse.store(Foo())
        foobar_test_factory.warehouse.store(Bar())
        await foobar_test_factory.take_over_foobar_market(foobar_test_factory.robots[0])
        self.assertTrue((
            foobar_test_factory.warehouse.get('foobar') == 1 and
            foobar_test_factory.warehouse.get('foo') == 6) and
            foobar_test_factory.warehouse.get('bar') == 0, "Foobar not assembled when resources available ")

    async def test_takeover_foobar_market(self):
        with open('tests/report.json') as f:
            report_result = json.load(f)
        report_test = await main(FoobarFactory(2), 5)
        self.assertEqual(report_result, report_test, "Process to take over market changed")

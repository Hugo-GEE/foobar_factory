import time
import math
import random
import configparser
import asyncio
from resources.factory import *

random.seed(42)



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
    return foobar_factory.report(final=True, json=True)


if __name__ == "__main__":
    asyncio.run(main(4))

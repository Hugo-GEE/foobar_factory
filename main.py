import time
import math
import random
import configparser
import asyncio
import logging
from resources.factory import *
from resources.tools import *

async def main(robots_to_finish:int = 30):
    """Instantiate Robots and produce foobars"""
    round_counter = 0
    foobar_factory = FoobarFactory()
    foobar_factory.add_robot()
    foobar_factory.add_robot()
    while len(foobar_factory.robots) < robots_to_finish:
        logging.debug(report(foobar_factory, round_counter))
        round_counter += 1
        await asyncio.gather(
                            *[foobar_factory.take_over_foobar_market(robot)
                            for robot in foobar_factory.robots])

    logging.info(report(foobar_factory, round_counter, final=True))
    logging.info("\nFoobar market domination achieved. Next, world.\n")
    return report(foobar_factory, round_counter, final=True, json=True)


if __name__ == "__main__":

    logging.getLogger('asyncio').setLevel(logging.WARNING)
    if args.get('verbose') == 'debug':
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    elif args.get('verbose') == 'info':
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(message)s')

    random.seed(SEED)

    asyncio.run(main(int(args['robots'])))

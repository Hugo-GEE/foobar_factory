"Orchestrates the program"

import random
import asyncio
import logging
from typing import List
import argparse
from resources.factory import FoobarFactory
from resources.tools import report, SEED

async def main(foobar_factory:FoobarFactory, robots_to_finish:int = 30) -> List[str]:
    """Instantiate Robots and produce foobars"""
    round_counter = 0
    while len(foobar_factory.robots) < robots_to_finish:
        logging.debug(report(foobar_factory, round_counter))
        round_counter += 1
        await asyncio.gather(
                            *[foobar_factory.take_over_foobar_market(robot)
                            for robot in foobar_factory.robots])

    logging.info(report(foobar_factory, round_counter, final=True))
    logging.info("\nFoobar market domination achieved. Next, world.\n")
    return report(foobar_factory, round_counter, json=True)


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--robots", required=False, help="Number of robots to attain foobar market domination")
    ap.add_argument("-v", "--verbose", required=False, help="Level of verbosity :'debug' or 'info' (none by default)")
    args = vars(ap.parse_args())

    logging.getLogger('asyncio').setLevel(logging.WARNING)
    if args.get('verbose') == 'debug':
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    elif args.get('verbose') == 'info':
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(message)s')

    random.seed(SEED)

    if 'robots' in args and args['robots'] is not None:
        asyncio.run(main(FoobarFactory(), int(args['robots'])))
    else:
        asyncio.run(main(FoobarFactory()))

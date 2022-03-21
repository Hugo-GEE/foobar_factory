"Contains some additional functions and config"

from __future__ import annotations
import configparser
import random
import time
import math


config = configparser.ConfigParser()
config.read("config")

SEED = int(config['PARAMS']['seed'])

random.seed(SEED)

ROBOT_NAMES = config['ROBOT_NAMES']['robot_names'].split(',')
random.shuffle(ROBOT_NAMES)
ROBOT_OFFSET = len(ROBOT_NAMES)

TIME_UNIT = float(config['PARAMS']['time_unit'])


def report(factory:FoobarFactory, round_counter:int, final:bool=False, json:bool=False)  -> str:
    "Produces a report of some key metrics of factory."
    round_counter = f"round {round_counter}"
    foobars = f"{factory.warehouse.get('foobar')} foobars"
    foo = f"{factory.warehouse.get('foo')} foo"
    cum_factory_time =  f"Cumulated factory time {round(sum(factory.clock)/60, 1)}min"
    cash = f"{factory.wallet}"
    robots = f"{len(factory.robots)} robots"
    parameters = [round_counter, cum_factory_time, foobars, foo, cash, robots]
    if final is True:
        real_time = f"Real time = {round(time.time() - factory.start_time, int(-math.log(TIME_UNIT)/3))}s"
        cpu_time = f"Process time = {round(time.process_time() - factory.start_cpu_time, int(-math.log(TIME_UNIT)/3))}s"
        cum_time =  f"Cumulated real time = {round(sum(factory.clock)*TIME_UNIT, int(-math.log(TIME_UNIT)/3))}s"
        parameters.remove(foobars)
        parameters.remove(cash)
        parameters.remove(cum_factory_time)
        parameters.remove(robots)
        parameters += [real_time, cpu_time, cum_time]
    if json is True:
        return parameters
    return '\n' + " | ".join(parameters) + "\n"

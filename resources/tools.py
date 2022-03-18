

VERBOSE = 'vvv'

def verboseprint(verbose_level, *args):
    if VERBOSE == 'vvv':
        print(*args)
    if VERBOSE == 'vv':
        if verbose_level == 'vv' or verbose_level == 'v':
            print(*args)
    if VERBOSE == 'v':
        if verbose_level == 'v':
            print(*args)

# Compatible with ranger 1.6.*
#
# This plugin adds the sorting algorithm called 'random'.  To enable it, type
# ":set sort=random" or create a key binding with ":map oz set sort=random"

from ranger.container.directory import Directory
from random import random
Directory.sort_dict['random'] = lambda path: random()


# RANDOM
import random
from random import choice

def generate_id(num):
    symbols = 'aSfzeKGhxAsBPYMECJmUwQgdcuRbXFHDkLvniytjNqpVWrTZ123456789'
    key = ''.join(choice(symbols) for i in range(num))
    return key
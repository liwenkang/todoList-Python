from utils import log
import random


def random_str():
    character = 'abcdefghijklmnopqlstuvwxyzABCDEFGHIJKLMNOPQLSTUVWXYZ0123456789'
    result = ''
    for i in range(16):
        random_index = random.randint(0, len(character) - 1)
        result += character[random_index]
    return result


random_str()

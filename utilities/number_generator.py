import random


def generate_random_number(length):

    if length < 1:
        raise ValueError("Length must be at least 1")

    start = 10 ** (length - 1)  # Smallest number with the given length
    end = 10 ** length - 1  # Largest number with the given length

    return random.randint(start, end)



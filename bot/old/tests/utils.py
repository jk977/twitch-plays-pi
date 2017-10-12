from random import randint

def pick_random_element(arr):
    return arr[randint(0, len(arr)-1)]

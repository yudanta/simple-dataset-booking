#!/usr/bin/env python 
import string
import random 

def generate_random_str(length=4):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters,length))
# -*- coding: utf-8 -*-

def echo(*args, **kwargs):
    """echo can be used to test how *args and **kwargs will be presented
    to Python functions."""
    return {
        'arguments': args,
        'keywords': kwargs,
    }

def add(a, *b):
    """Add numbers"""
    for v in b:
        a = a + v
    return a

def sub(a, b):
    """Subtract one number from another"""
    return a - b


def echo(*args, **kwargs):
    """echo can be used to test how *args and **kwargs will be presented
    to Python functions."""
    return {
        'arguments': args,
        'keywords': kwargs,
    }

def add(a, b):
    """Add two numbers"""
    return a + b

def sub(a, b):
	"""Subtract one number from another"""
	return a - b
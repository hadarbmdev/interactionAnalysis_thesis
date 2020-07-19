#import libraries
import numpy as np
import mxnet as mx
import os
mx.random.seed(1)
# Define the context to be CPU
ctx = mx.cpu()

# function to encode the integer to its binary representation


def binary_encode(i, num_digits):
    return np.array([i >> d & 1 for d in range(num_digits)])

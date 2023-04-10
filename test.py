import numpy as np

A = np.random.randn(4,3)

B = np.sum(A, axis = 1, keepdims = True) 

print(B.shape)
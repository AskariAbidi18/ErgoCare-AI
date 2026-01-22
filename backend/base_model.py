import numpy as np

"""
Just a base scalable feedforward model implementation with Layer, Dense, Activation and Model classes.
Needs to be scaled to a full framework later according to requirements.
"""

class Layer:
  def forward(self, X):
    raise NotImplementedError("forward() not implemented")
  def backward(self, grad):
    raise NotImplementedError("backward() not implemented")
  def params(self):
    return []
  def grads(self):
    return []

class Dense(Layer):
  def __init__(self, input_dim, output_dim):
    self.W = np.random.randn(input_dim, output_dim)
    self.b = np.zeros((1,output_dim))
  def forward(self, X):
    self.X_cache = X
    return X @ self.W + self.b
  def backward(self, grad):
    self.dW = self.X_cache.T @ grad
    self.db = np.sum(grad, axis = 0, keepdims = True)
    return grad @ self.W.T
  def params(self):
    return [self.W, self.b]
  def grads(self):
    return [self.dW, self.db]

class Activation(Layer):
  def __init__(self, func, func_prime):
    self.func = func
    self.func_prime = func_prime
  def forward(self, X):
    self.X_cache = X
    return self.func(X)
  def backward(self, dA):
    return dA * self.func_prime(self.X_cache)
  
class Model:
  def __init__(self, layers):
    self.layers = layers
  def forward(self, X):
    for layer in self.layers:
      X = layer.forward(X)
    return X
  def backward(self, grad):
    for layer in reversed(self.layers):
      grad = layer.backward(grad)
  def params_and_grads(self):
    for layer in self.layers:
      for (p, g) in zip(layer.params(), layer.grads()):
        yield (p, g)
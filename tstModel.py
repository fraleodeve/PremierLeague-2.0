from model.model import Model

m = Model()
m.buildGraph(0.5)
n, ar = m.getDetails()
print(n)
print(ar)

a, b = m.getBestPath(3)
print(a)
print(b)

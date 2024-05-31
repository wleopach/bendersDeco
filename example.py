# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints.   The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.  The lazy constraint callback
# adds new constraints to cut them off.

import sys
import math
import random
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB
from plot import plot_sol, plot_sol_with_subtour

# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)

        # find the shortest cycle in the selected edge list
        tour = subtour(vals)
        if len(tour) < n:
            plot_sol(points, vals, "Current Solution")
            plot_sol_with_subtour(points, vals, tour)
            # Construct the lazy constraint expression
            lazy_expr = gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2))
            lazy_constraint = (lazy_expr <= len(tour) - 1)

            # Add lazy constraint
            model.cbLazy(lazy_constraint)

            # Print the lazy constraint
            print(f"Lazy constraint added: {lazy_constraint}")



# Given a tuplelist of edges, find the shortest subtour

def subtour(vals):
    # make a list of edges selected in the solution
    edges = gp.tuplelist((i, j) for i, j in vals.keys()
                         if vals[i, j] > 0.5)
    unvisited = list(range(n))
    cycle = range(n+1)  # initial length has 1 more city
    while unvisited:  # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*')
                         if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle


# Parse argument

# if len(sys.argv) < 2:
#     print('Usage: tsp.py npoints')
#     sys.exit(1)
# n = int(sys.argv[1])
n = 40
# Create n random points

random.seed(1)
points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(n)]

# Dictionary of Euclidean distance between each pair of points

dist = {(i, j):
        math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
        for i in range(n) for j in range(i)}

m = gp.Model()

# Create variables

vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
# Add reverse direction edges separately to avoid modifying the dictionary during iteration
for i, j in list(vars.keys()):
    vars[j, i] = vars[i, j]

# You could use Python looping constructs and m.addVar() to create
# these decision variables instead.  The following would be equivalent
# to the preceding m.addVars() call...
#
# vars = tupledict()
# for i,j in dist.keys():
#   vars[i,j] = m.addVar(obj=dist[i,j], vtype=GRB.BINARY,
#                        name='e[%d,%d]'%(i,j))


# Add degree-2 constraint

m.addConstrs(vars.sum(i, '*') == 2 for i in range(n))

# Using Python looping constructs, the preceding would be...
#
# for i in range(n):
#   m.addConstr(sum(vars[i,j] for j in range(n)) == 2)


# Optimize model

m._vars = vars
m.Params.LazyConstraints = 1
m.optimize(subtourelim)

vals = m.getAttr('X', vars)
tour = subtour(vals)
plot_sol(points, vals, "Final Solution")
assert len(tour) == n

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.ObjVal)
print('')

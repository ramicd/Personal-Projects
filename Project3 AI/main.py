


from gui import *
from problem import *
from solver import *

attributes,constraints,preferences = gui()

problem = Problem(attributes, constraints, preferences)
problem.getAttributes()
problem.getConstraints()
problem.getPreferences()
problem.writeConstraints()

solver = Solver(problem)
solver.runClasp()
solver.getFeasibleModels()
solver.whichLogic()
solver.calculatePreferences()
solver.twoRandomModels()
solver.optimization()
solver.omniOptimization()
solver.toString()

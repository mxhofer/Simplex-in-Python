__author__ = "maxhofer"

"""Entirely self-written testing framework."""

from Simplex_Algorithm import Simplex
# import Simplex class from the Simplex_Algorithm.py file, which both need to be in the same directory

import random  # import random package used to create randomised linear programming problems
from scipy.optimize import linprog  # import function .linprog from the python package scipy.optimize
import numpy as np  # import numpy package used to prepare matrix/vector inputs A, b and c


def testmodel(nodecvar, noconstraints):
    # purpose: create a random linear programming problem and compare result of my code with Python's .linprog
    # function and reuse code in timing file; input: number of decision variables and constraints;
    # output: workings and result of my code and of .linprog

    if nodecvar < 1 or noconstraints < 1:  # at least 1 decision variable and constraint required
        raise ValueError("The number of decision variables and constraints needs to be larger than 0.")

    constraintlhs = []
    # empty list to store the lhs of a constraint; required as data instance to be used by .linprog function

    constraintrhs = []
    # empty list to store the rhs of a constraint; required as data instance to be used by .linprog function

    testobj = [random.randint(-20, 20) for _ in range(nodecvar)]
    # create a variable to store the randomly generated objective function

    test = Simplex(testobj)  # create an instance of Simplex given the test objective function as the parameter

    for _ in range(noconstraints):
        # loop to append as many lhs and rhs instances to the list as there are decision variables; other number of
        # constraints worked equally well in testing, so just change "range(nodecvar)" to a different value

        constraintlhs.append([random.randint(0, 20) for _ in range(nodecvar)])
        # only non negative lhs constraint values, because linear constraints can otherwise lie in the negative space,
        # which would yield a negative objective value; starting from 0 also works

        constraintrhs.append(random.randint(1, 20))
        # only positive rhs constraint values, because resource constraints are generally available in
        # positive quantities; starting from 0 may result in a logical error

    for index in range(noconstraints):  # loop to add as many constraints as there are decision variables
        test.add_constraint(constraintlhs[index], constraintrhs[index])  # add constraints to the test instance

    test.solve()  # call the .solve method of the Simplex class to solve the test problem

    # set up data for .linprog function

    A = np.mat(constraintlhs)  # turn the list of lists constraintlhs into an np.matrix input for .linprog
    b = np.array(constraintrhs) # np.array to prepare matrix/vector inputs A, b, c
    c = np.array([i*(-1) for i in testobj])
    # change sign of each list element, because standard form of z = a x1 + b x2 is required, not z - a x1 - b x2 = 0
    # np.array to prepare matrix/vector inputs A, b, c

    result = linprog(c*(-1), A, b,  method="simplex")  # as .linprog minimises objective function, c is multiplied by -1

    print("\nmax =  ", -result.fun, "\nat x = ", result.x, "\n--> .linprog result")
    # outputs maximum at optimal solution and respective x-values

    # concluding statement to confirm with .linprog that the result of my algorithm is correct

    if -result.fun == test.obj[-1] and list(result.x) == test.solutionvalues():
        # conditional to check if the max of objective function and the x-values of both methods are equal

        print("\nResult correct, confirmed by .linprog function: z={0:.3g} at x={1}".format
            (-result.fun, ['%.2f' % elem for elem in list(result.x) ]))
        # if they are, it prints a confirmation and restates the optimal solution and respective x-values

    else:
        print("Result incorrect, likely due to rounding errors. Try a different example.")


testmodel(3, 8)
# call the testing function to run a test with a specified number of decision variables and number of constraints

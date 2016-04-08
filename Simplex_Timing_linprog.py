__author__ = "maxhofer"

"""Entirely self-written file. The testmodel() function is adapted from Simplex_Testing_Random.py in order to
prepare data for linprog function."""

import time  # to take the start and end times
import statistics  # to calculate the mean time
import random  # to create random objective functions and contraints
import numpy as np  # import numpy package used to prepare matrix/vector inputs A, b and c
from scipy.optimize import linprog  # import function .linprog from the python package scipy.optimize


def testmodel(nodecvar, noconstraints):
    # purpose: create a random linear programming problem and time it;
    # input: number of decision variables and constraints;
    # output: result of my code compared to result of .linprog function

    if nodecvar < 1 or noconstraints < 1:  # conditional to catch wrong input and raise an error
        raise ValueError("The number of decision variables and constraints needs to be larger than 0.")

    constraintlhs = []
    # empty list to store the lhs of a constraint; required as data instance to be used by .linprog function

    constraintrhs = []
    # empty list to store the rhs of a constraint; required as data instance to be used by .linprog function

    testobj = [random.randint(-20, 20) for _ in range(nodecvar)]
    # create a variable to store the randomly generated objective function

    for _ in range(noconstraints):
        # loop to append as many lhs and rhs instances to the list as there are decision variables; other number of
        # constraints worked equally well in testing, so just change "range(nodecvar)" to a different value

        constraintlhs.append([random.randint(0, 20) for _ in range(nodecvar)])
        # only non negative lhs constraint values, because linear constraints can otherwise lie in the negative space,
        # which would yield a negative objective value; starting from 0 also works

        constraintrhs.append(random.randint(1, 20))
        # only positive rhs constraint values, because resource constraints are generally available in
        # positive quantities; starting from 0 may result in a logical error

    A = np.mat(constraintlhs)  # turn the list of lists constraintlhs into an np.matrix input for .linprog
    b = np.array(constraintrhs) # np.array to prepare matrix/vector inputs A, b, c
    c = np.array([i*(-1) for i in testobj])
    # change sign of each list element, because standard form of z = a x1 + b x2 is required, not z - a x1 - b x2 = 0
    # np.array to prepare matrix/vector inputs A, b, c

    result = linprog(c*(-1), A, b,  method="simplex")  # as .linprog minimises objective function, c is multiplied by -1

    print("\nmax =  ", -result.fun, "\nat x = ", result.x, "\n--> .linprog result")

# original timing function from seminar notes

times = []
for _ in range(50):  # takes 50 individual times
    startTime = time.time()  # start time
    testmodel(4, 4)  # change parameters
    endTime = time.time()  # end time
    times.append(endTime-startTime)  # add the time taken
print("Mean time in seconds:", statistics.mean(times))  # print the mean time

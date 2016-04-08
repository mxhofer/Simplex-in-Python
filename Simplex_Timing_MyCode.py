__author__ = "maxhofer"

"""Takes times of my code solving a randomly generated linear programming problem. The testmodel() function is adapted
from Simplex_Testing_Random.py in order to exclude .linprog function."""

from Simplex_Algorithm import Simplex
# import Simplex class from the Simplex_Algorithm.py file, which both need to be in the same directory

import time
import statistics
import random

def testmodel(nodecvar, noconstraints):
    # purpose: create a random linear programming problem
    # function and reuse code in timing file; input: number of decision variables and constraints;
    # output: workings and result of my code

    if nodecvar < 1 or noconstraints < 1:  # at least 1 decision variable and constraint required
        raise ValueError("The number of decision variables and constraints needs to be larger than 0.")

    constraintlhs = []
    # empty list to store the lhs of a constraint; required as data instance

    constraintrhs = []
    # empty list to store the rhs of a constraint; required as data instance

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

    test.solve()

# original timing function from seminar notes

times = []
for _ in range(50):  # takes 50 individual times
    startTime = time.time()  # start time
    testmodel(4, 4)  # change parameters
    endTime = time.time()  # end time
    times.append(endTime-startTime)  # add the time taken
print("Mean time in seconds:", statistics.mean(times))  # print the mean time

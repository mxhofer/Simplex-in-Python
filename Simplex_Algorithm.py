__author__ = "maxhofer"

"""Simplex algorithm basic code (Python 2.x) from: http://hubpages.com/technology/Simplex-Algorithm-in-Python.
Note: row 0 corresponds to row 0 in our lecture slides and not in python language"""

from numpy import *  # imports everything from numpy without prefixing


class Simplex(object):  # Simplex class used to abstract and decompose the algorithm into various methods

    def __init__(self, obj):
        # __init__ is a constructor, which initialises an instance of a class; input: objective function;
        # output: initialised instance of a class

        self.obj = [1] + obj  # list incl. objective function; 1 stands for z value equal to 1 in row 0 of augm. matr.
        self.rows = []  # empty list with lhs of constraints for the augmented matrix form
        self.cons = []  # empty list for rhs values of constraints
        self.decvar = obj  # !stores the decision variables in the objective function as a list

    def add_constraint(self, lhsexpression, rhsvalue):
        # used to add constraint; input: lhs and rhs of constraint in the general form x+y <= c -> [x, y] <= [rhsvalue];
        # add_constraints([lhs], rhsvalue); output: stores constraint in

        self.rows.append([0] + lhsexpression)  # 0 stands for z value column, lhsexpression for lhs of constraints
        self.cons.append(rhsvalue)  # !value equals the rhs value of the constraint

    def pivot_column(self):
        # identifies index of pivot column; input (not as parameter, but in the method's for loop):
        # objective function (i.e. row 0); output: index of pivot column

        low, idx = 0, 0  # !two variables are used to see which values of row 0 are non negative
        for i in range(1, len(self.obj)-1):
            # loops through decision variables in row 0; -1 because list starts at index 0
            if self.obj[i] < low:  # conditional that holds true for negative entries in row 0
                low = self.obj[i]  # sets low to the lowest negative coefficient value
                idx = i  # sets idx to the index of entering variable (EV), i.e. largest negative coefficient in row 0
        if idx == 0:
            return -1  # if idx remains 0, i.e. no negative value in row 0, -1 is returned
        return idx

    def pivot_row(self, col):
        # identifies index of pivot row; input: pivot column; output: smallest value of rhs/evc

        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        # creates list of right most column in augmented matrix

        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        # creates list by recursively calling items in rows except row 0 in the pivot column, col

        ratio = []  # empty list for ratios of (RHS of row i)/(entering value coefficient of row i)
        for i in range(len(rhs)):  # starts with zero up to, but not including, the number of items in rhs list
            if lhs[i] == 0:  # conditional to avoid a ZeroDivisionError
                ratio.append(99999999 * abs(max(rhs)))  # appends a huge number in order to make sure not to choose it
                continue
            ratio.append(rhs[i]/lhs[i]) # appends values to RHS/EVC column
        try: lowestratio = min(i for i in ratio if i > 0)  # !finds the lowest positive ratio
        except: raise ValueError("RHS/EVC ratios are all negative. Try a different example.")  # very very rare case
        return ratio.index(lowestratio)  # !returns index of smallest positive value of RHS/EVC

    def pivot(self, row, col):  # Gauss-Jordan row operations around pivot point; input: row and column index to
                                # specify pivot point; output: modifies class instance (i.e. objective function and
                                # rows in augmented matrix)
        pivotpoint = self.rows[row][col]  # !define the pivot point
        self.rows[row] /= pivotpoint  # change pivot point to 1 by dividing the respective row by the pivot point value
        self.obj = self.obj - self.obj[col]*self.rows[row]  # sets entry above pivot point in row 0 equal to 0
        for r in range(len(self.rows)):  # loops through augmented matrix entries above and below pivot row
            if r == row:
                continue  # skips the pivot row
            self.rows[r] = self.rows[r] - self.rows[r][col]*self.rows[row]
            # sets entries below pivot point equal to 0, except for row 0 itself

    def solutionvalues(self):  # entirely self-coded method. print x-values of optimal solution, input: all constraints,
        # output: list of x-values at optimal point

        xlist = [0] * len(self.decvar)
        # list of 0's with length equal to number of decision variables to eventually output solution values

        for i in range(len(self.rows)):  # loop to iterate over each row except row 0
            for x in range(len(self.rows[i])):  # loop to iterate over each column of self.rows[i]
                while x < len(xlist):  # the 1 can only be in the (number of decision variables)+1 columns
                    if self.rows[i][x+1] == 1 and self.is_unit_column(x+1):
                        # if the entry is equal to 1 AND the column is a unit column

                        xlist[x] = self.rows[i][-1]  # if this is the case, it adds the last row item to xlist
                    x += 1  # makes while loop inspect the next element in row i
                break  # breaks the second for loop to go back to the first for loop and increase i by 1
        return xlist

    def is_unit_column(self, col):  # entirely self-coded method.
        #  checks if a specific column is a unit column; input: column index; output: boolean True or False

        row_iterator = 0  # variable to iterate through rows in self.rows
        columnsum = 0 + self.obj[col]  # sum that equals 1 if its a unit column
        while row_iterator < len(self.cons):  # loops through number of constraints, i.e. number of rows to be checked
            columnsum += self.rows[row_iterator][col]  # calculates the sum of each element in column col
            row_iterator += 1  # 1 is added to iterator variable to check the next row
        if columnsum == 1:  # conditional that returns True if the sum of column entries equals 1
            return True
        else:  # conditional that returns False if sum of column entries equals a different value than 1
            return False

    def row0_check(self):
        # checks if coefficients of decision and slack variables in row 0 are all non negative; outputs boolean operator
        if min(self.obj[1:-1]) >= 0:
            return 1
        # checks all entries except very first one, which must equal 1 anyway; 1 means Boolean true

        else:
            return 0  # returns a 0 (i.e. boolean False) to reiterate because optimal solutions has not been found yet

    def display(self):
        # prints augmented matrix of objective function and constraints first, then each augmented matrix iteration
        # input: data stored in class instance; output: matrix representation and z values at each iteration

        print('\nMatrix form:\n', matrix([self.obj] + self.rows), '\n\n', 'z = {}'.format(self.obj[-1]))
        # !prints matrix and z value at each iteration

    def solve(self):
        # method to solve LP problem; input: self. data in class instance; output: print simplex iterations and solution

        iterationCounter = 0

        # build augmented matrix tableau
        for rowindex in range(len(self.rows)):  # !loop to store rows 1 to i, including slack variables
            self.obj += [0]  # adds zeroes to row 0 to be of the same length as rows 1 to i

            slackvar = [0 for _ in range(len(self.rows))]
            # !creates list of 0's with length equal to number of constraints, equalling the number of slack variables

            slackvar[rowindex] = 1  # !replaces diagonal slack variable terms with 1

            self.rows[rowindex] += slackvar + [self.cons[rowindex]]
            # !creates complete rows 1 to i by adding slack variables and the rhs value of the constraints

            self.rows[rowindex] = array(self.rows[rowindex], dtype=float)
            # !set rows 1 to i to an array (from the numpy package) including constraints, slack variables and
            # rhs of constraints as floats

        self.obj = array(self.obj + [0], dtype=float)
        # set row 0 to an array including additional 0 as there's no self.cons (i.e. rhs value)
        # for row 0, with all entries as floats

        self.display()
        # prints initial augmented matrix with all coefficients
        # and slack variables being non negative by calling .display() method specified above

        while not self.row0_check():  # repeat the method (i.e. self.check method returns 0)
            iterationCounter += 1  # counts the iterations

            pivotcol = self.pivot_column()
            # !pivotcol equals the index of the pivot column minus 1 (python lists start at 0)

            pivotrow = self.pivot_row(pivotcol)
            # !pivotrow equals pivot row at column pivotcol minus 2 (python lists start at zero and
            # self.pivot_row() method does not include row 0

            self.pivot(pivotrow, pivotcol)  # calls .pivot() method, for row r and column c

            print('\niteration: {}\npivot column: {}\npivot row: {}'.format(iterationCounter, pivotcol+1, pivotrow+2))
            # c+1 and r+2 to compensate for python list starting at 0 and row 0 is not included in self.pivot_row()
            # method respectively

            self.display()  # prints augmented matrix with all coefficients

        if self.row0_check():  # !prints the x values of the optimal solution once the last iteration has been performed
            print("at x =", self.solutionvalues(), "\n--> my result")

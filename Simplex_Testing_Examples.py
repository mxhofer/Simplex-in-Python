__author__ = "maxhofer"

"""General examples with solutions found in textbooks, online and in our lecture slides.
Entirely self-coded file. Uncomment the .solve() method to test."""

from Simplex_Algorithm import Simplex
# import Simplex class from the Simplex_Algorithm.py file, which both need to be in the same directory

t = Simplex([-2,-3,-2])  # from: http://hubpages.com/technology/Simplex-Algorithm-in-Python
t.add_constraint([2, 1, 1], 4)
t.add_constraint([1, 2, 1], 7)
t.add_constraint([0, 0, 1], 5)
# t.solve()
# given solution: z=11, [0,3,1] - correct


u = Simplex([-3,-5])  # from:  MFoM III Linear Programming Lecture 2 slide set
u.add_constraint([0, 2], 12)
u.add_constraint([3, 2], 18)
# u.solve()
# given solution: z=36, [2,6] - correct


v = Simplex([-3, -2])  # from: http://www.phpsimplex.com/en/simplex_method_example.htm
v.add_constraint([2,1], 18)
v.add_constraint([2,3], 42)
v.add_constraint([3,1], 24)
# v.solve()
# given solution: z=33, [3,12] - correct
# works well as I've restricted picking only the smallest POSITIVE RHS/EVC value


w = Simplex([-3, -5])  # from: ftp://ftp.ti.com/pub/graph-ti/calc-apps/86/math/simplex.txt
w.add_constraint([1, 0], 4)
w.add_constraint([0, 2], 12)
w.add_constraint([3, 2], 18)
# w.solve()
# given solution: z=36, [2,6] - correct


x = Simplex([-3, -4])  # from: http://www.ms.uky.edu/~rwalker/class%20work%20solutions/class%20work%208%20solutions.pdf
x.add_constraint([1, 1], 4)
x.add_constraint([2, 1], 5)
# x.solve()
# given solution: z=16, [0,4] - correct


# initially a min problem from: http://www.ms.uky.edu/~rwalker/class%20work%20solutions/class%20work%208%20solutions.pdf
y = Simplex([-2, 1])
y.add_constraint([1, 2], 6)
y.add_constraint([3, 2], 12)
# y.solve()
# given solution: z=8, [4,0] - correct


z = Simplex([-40, -50])  # from: http://wps.prenhall.com/wps/media/objects/1159/1186960/cdrom_modules/module_a1.pdf
z.add_constraint([1, 2], 40)
z.add_constraint([4, 3], 120)
# z.solve()
# given solution: z=1360, [24,8] - correct

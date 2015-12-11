EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Susan Sim"
__license__ = "MIT License"


#####################
# HELPER FUNCTIONS ##
#####################
def remove_duplicates(l):
    """
    Removes duplicates from l, where l is a List of Lists.
    :param l: a List
    """

    d = {}
    result = []
    for row in l:
        if tuple(row) not in d:
            result.append(row)
            d[tuple(row)] = True

    return result


class UnknownAttributeException(Exception):
    """
    Raised when attempting set operations on a table
    that does not contain the named attribute
    """
    pass

# EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
#              ["Smith", "Mary", 25, 2000],
#              ["Black", "Lucy", 40, 3000],
#              ["Verdi", "Nico", 36, 4500],
#              ["Smith", "Mark", 40, 3900]]
#
#
# def filter_employees(row):
#     """
#     Check if employee represented by row
#     is AT LEAST 30 years old and makes
#     MORE THAN 3500.
#     :param row: A List in the format:
#         [{Surname}, {FirstName}, {Age}, {Salary}]
#     :return: True if the row satisfies the condition.
#     """
#     return row[-2] >= 30 and row[-1] > 3500


def selection(t1, f):
    """
    Perform select operation on table t that satisfy condition f.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True iff
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]

    """
    i = 1
    result = []
    pass
    result.append(t1[0])
    while i < len(t1):
        if f(t1[i]):
            result.append(t1[i])
        i += 1
    if len(result) == 1:
        result = None
    return result


# GRADUATES = [["Number", "Surname", "Age"],
#              [7274, "Robinson", 37],
#              ["Surname", "O'Malley", 39],
#              [9824, "Darkes", 38]]


def projection(t, r):
    """
    Perform projection operation on table t
    using the attributes subset r.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """
    # i tracks the spot for the attribute list
    i = 0
    # j tracks which row within the table is being compared
    j = 0
    # k tracks which item within the row is being compared
    k = 0
    result = []
    try:
        while i < len(r):
            while k < len(t[j]):
                if r[i] == t[j][k]:
                    while j < len(t):
                        result.append([t[j][k]])
                        j += 1
                j = 0
                k += 1
            k = 0
            i += 1
    except AssertionError:
        raise UnknownAttributeException

    print result


def cross_product(t1, t2):
    """
    Return the cross-product of tables t1 and t2.

    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]

    """
    i = 1
    j = 1
    result = []
    pass

    result = [t1[0] + t2[0]]
    while i < len(t1):
        while j < len(t2):
            result.append(t1[i]+t2[j])
            j += 1
        j = 1
        i += 1
    if len(result) == 1:
        result = None

    return result

#projection(EMPLOYEES, ["Surname", "FirstName"])
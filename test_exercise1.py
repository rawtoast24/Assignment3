#!/usr/bin/env python

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

Test module for exercise3.py

"""

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Susan Sim"
__license__ = "MIT License"

from exercise1 import selection, projection, cross_product


###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]

R3 = [[]]

#####################
# HELPER FUNCTIONS ##
#####################

def is_equal(t1, t2):
    return sorted(t1) == sorted(t2)


#####################
# FILTER FUNCTIONS ##
#####################
def filter_employees(row):
    """
    Check if employee represented by row
    is AT LEAST 30 years old and makes
    MORE THAN 3500.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition.
    """
    return row[-2] >= 300 and row[-1] > 3500


def intersection(table1, table2):
    """
    Established intersection function to perform the intersection set operation on tables 1 and 2. Table 3 variable is
    established to represent the unique rows that appear in both table 1 and table 2.

    :param table1: a table (a List of Lists)
    :param table2: a table (a List of Lists)
    :return: table3: a table with the header from table1/table2 and unique rows that appear in both tables
    :raises: MismatchedAttributesException:
        if tables table1 and table2 don't have the same attributes
    """
    table3 = []
    i = 0
    j = 0
    if table1[0] != table2[0]:
        raise Exception("MismatchedAttributesException")
    else:
        while i < len(table1):
            while j < len(table2):
                if table1[i] == table2[j]:
                    table3.append(table2[j])
                    j += 1
                else:
                    j += 1
            j = 0
            i += 1

    if len(table3) == 1:
        table3 = None
    return table3



###################
# TEST FUNCTIONS ##
###################


def test_selection():
    """
    Test select operation.
    """

    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500],
              ["Smith", "Mark", 40, 3900]]

    assert selection(R1, filter_employees) is None
    assert selection(R3, filter_employees) is None
    assert is_equal(result, selection(EMPLOYEES, filter_employees))

def test_projection():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]

    assert is_equal(result, projection(EMPLOYEES, ["Surname", "FirstName"]))


def test_cross_product():
    """
    Test cross product operation.
    """

    result = [["Employee", "Department", "Department", "Head"],
              ["Smith", "sales", "production", "Mori"],
              ["Smith", "sales", "sales", "Brown"],
              ["Black", "production", "production", "Mori"],
              ["Black", "production", "sales", "Brown"],
              ["White", "production", "production", "Mori"],
              ["White", "production", "sales", "Brown"]]

    assert is_equal(result, cross_product(R1, R2))
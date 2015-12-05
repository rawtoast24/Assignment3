#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Susan Sim"
__license__ = "MIT License"

import re
import datetime
import json

######################
## global constants ##
######################
REQUIRED_FIELDS = ["passport", "first_name", "last_name",
                   "birth_date", "home", "entry_reason", "from"]

######################
## global variables ##
######################
'''
countries:
dictionary mapping country codes (lowercase strings) to dictionaries
containing the following keys:
"code","name","visitor_visa_required",
"transit_visa_required","medical_advisory"
'''
COUNTRIES = None


#####################
# HELPER FUNCTIONS ##
#####################
def is_more_than_x_years_ago(x, date_string):
    """
    Check if date is less than x years ago.

    :param x: int representing years
    :param date_string: a date string in format "YYYY-mm-dd"
    :return: True if date is less than x years ago; False otherwise.
    """

    now = datetime.datetime.now()
    x_years_ago = now.replace(year=now.year - x)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    return (date - x_years_ago).total_seconds() < 0


def decide(input_file, countries_file):
# def decide(input_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """
   # convert the entry record from JSON into Python
    with open(input_file,"r") as file_reader:
        file_contents = file_reader.read()

    entry_record = json.loads(file_contents)

    # convert the list of countries from JSON into Python
    with open(countries_file, "r") as country_reader:
        country_contents = country_reader.read()

    country_dictionary = json.loads(country_contents)

    #check if the entry record is complete; rejects if it isn't
    i = 0
    j = 1
    decision = []
    result = []
    for key in entry_record[0]:
        if entry_record[0][key] == "":
            decision.append("Reject")
        else:
            decision.append("Accept")

    # Cleans up the decision list. Might not be necessary - check later
    while i < len(decision):
        while j < len(decision):
            if decision[i] == decision[j]:
                decision.remove(decision[j])
            j += 1
        j = 1
        i += 1


    # check if country is known or unknown; reject if latter
    country_list = []
    for key in country_dictionary:
        country_list.append(key)

    if entry_record[0]["from"]["country"] not in country_list:
        decision.append("Reject")


    # Iterate through the decision list and decide if person should be quarantined, rejected, or accepted
    if "Quarantine" in decision:
        result.append("Quarantine")
    elif "Reject" in decision:
        result.append("Reject")
    else:
        result.append("Accept")

    # Automatically allow KAN natives back in

    if entry_record[0]["home"]["country"] == "KAN":
        result = ["Accept"]

    return result
print decide("Entry Record.json","countries.json")


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    return False


def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """

    return False


"""
to get the keys of a dictionary, keys = dictionary.keys()
to check for empty strings, run a while loop checking for dictionary[keys[i]]
"""
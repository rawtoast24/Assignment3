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
    # create a list to store the decision for each record
    result = []
    # Used to iterate through the entry records
    a = 0

    # Convert the entry record from JSON into Python
    with open(input_file,"r") as file_reader:
        file_contents = file_reader.read()

    entry_record = json.loads(file_contents)

    # convert the list of countries from JSON into Python
    with open(countries_file, "r") as country_reader:
        country_contents = country_reader.read()

    country_dictionary = json.loads(country_contents)

    # Create a list of country codes
    country_list = []
    for key in country_dictionary:
        country_list.append(key)

    # Create a list of countries with medical alerts
    medical_alert = []
    for country in country_dictionary:
        if country_dictionary[country]["medical_advisory"] != "":
            medical_alert.append(country_dictionary[country]["code"])
    while a < len(entry_record):
        # create a list to store the decision for each check within a record
        decision = []
        # Step 1. check for missing information
        b = 0
        for key in entry_record[a]:
            if entry_record[a][key] == "":
                decision.append("Reject")
            else:
                decision.append("Accept")
            while b < len(entry_record[a][key]):
                if entry_record[a][key][b] == "":
                    decision.append("Reject")
                else:
                    decision.append("Accept")
                b += 1
        # Step 2. Check all locations
        if entry_record[a]["from"]["country"] not in country_list:
            decision.append("Reject")
        if entry_record[a]["home"]["country"] not in country_list:
            decision.append("Reject")
        if "via" in entry_record[a]:
            if entry_record[a]["via"] not in country_list:
                decision.append("Reject")
        # Step 3. Accept all returning KAN citizens
        if entry_record[a]["home"]["country"] == "KAN":
            decision.append("Accept")
        # Step 4. Check if any visitors have a valid visa
        if entry_record[a]["entry_reason"] == "visit":
            if is_more_than_x_years_ago(2,entry_record[a]["visa"]["date"]):
                decision.append("Reject")
        # Step 5. Check if anyone is coming from a country with a medical alert
        if entry_record[a]["from"]["country"] in medical_alert:
            decision.append("Quarantine")

        # Come up with a final decision
        if "Quarantine" in decision:
            result.append("Quarantine")
        elif "Reject" in decision:
            result.append("Reject")
        else:
            result.append("Accept")

        # Iterate to the next record
        a += 1

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
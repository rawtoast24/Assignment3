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

def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    count = 0
    passport_number = passport_number.upper()
    correct = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
               "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    decisions = []
    if len(passport_number) == 29:
        while count < 5:
            if passport_number[count] in correct:
                decisions.append("True")
            else:
                decisions.append("False")
            count += 1
        count = 6
        while count < 11:
            if passport_number[count] in correct:
                decisions.append("True")
            else:
                decisions.append("False")
            count += 1
        count = 12
        while count < 17:
                if passport_number[count] in correct:
                    decisions.append("True")
                else:
                    decisions.append("False")
                count += 1
        count = 18
        while count < 22:
                if passport_number[count] in correct:
                    decisions.append("True")
                else:
                    decisions.append("False")
                count += 1
        count = 24
        while count < 29:
                if passport_number[count] in correct:
                    decisions.append("True")
                else:
                    decisions.append("False")
                count += 1
        count = 5
        while count < len(passport_number):
            if passport_number[count] == "-":
                decisions.append("True")
            else:
                decisions.append("False")
            count += 6
        if "False" in decisions:
            result = False
        else:
            result = True
    else:
        result = False
    return result


def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """
    count = 0
    visa_code = visa_code.upper()
    correct = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
               "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    decisions = []
    if len(visa_code) == 11:
        while count < 5:
            if visa_code[count] in correct:
                decisions.append("True")
            else:
                decisions.append("False")
            count += 1
        count = 6
        while count < 11:
            if visa_code[count] in correct:
                decisions.append("True")
            else:
                decisions.append("False")
            count += 1
        if visa_code[5] == "-":
            decisions.append("True")
        else:
            decisions.append("False")

        if "False" in decisions:
            result = False
        else:
            result = True
    else:
        result = False
    return result

def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    correct = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    numbers = [0, 1, 2, 3, 5, 6, 8, 9]
    decisions = []

    if len(date_string) == 10:
        for i in numbers:
            if date_string[i] in correct:
                decisions.append("True")
            else:
                decisions.append("False")
        if date_string[4] and date_string[7] == "-":
            decisions.append("True")
        else:
            decisions.append("False")
        if "False" in decisions:
            result = False
        else:
            result = True
    else:
        result = False
    return result


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
        for key in entry_record[a]:
            if entry_record[a][key] == "":
                decision.append("Reject")
            else:
                decision.append("Accept")
        for key in entry_record[a]["home"]:
            if entry_record[a]["home"][key] =="":
                decision.append("Reject")
            else:
                decision.append("Accept")
        for key in entry_record[a]["from"]:
            if entry_record[a]["from"][key] =="":
                decision.append("Reject")
            else:
                decision.append("Accept")
        if "visa" in entry_record[a]:
            for key in entry_record[a]["visa"]:
                if entry_record[a]["visa"][key] =="":
                    decision.append("Reject")
                else:
                    decision.append("Accept")
        # Step 2. Check all locations
        if entry_record[a]["from"]["country"] not in country_list:
            decision.append("Reject")
        if entry_record[a]["home"]["country"] not in country_list and not "KAN":
            decision.append("Reject")
        if "via" in entry_record[a]:
            if entry_record[a]["via"] not in country_list:
                decision.append("Reject")
        # Step 3. Accept all returning KAN citizens
        if entry_record[a]["home"]["country"] == "KAN":
            decision.append("Accept")
        # Step 4. Check if any visitors have a valid visa
        if entry_record[a]["entry_reason"] == "visit":
            if valid_date_format(entry_record[a]["visa"]["date"]):
                if is_more_than_x_years_ago(2,entry_record[a]["visa"]["date"]):
                    decision.append("Reject")
        # Step 5. Check if anyone is coming from a country with a medical alert
        if entry_record[a]["from"]["country"] in medical_alert:
            decision.append("Quarantine")

        # Check for valid Passport Number Format
        if valid_passport_format(entry_record[a]["passport"]):
            decision.append("Accept")
        else:
            decision.append("Reject")

        # Check for valid Visa Number Format
        if entry_record[a]["entry_reason"] == "visit":
            if valid_visa_format(entry_record[a]["visa"]["code"]):
                decision.append("Accept")
            else:
                decision.append("Reject")

        # Check for valid Birth Date Format
        if valid_date_format(entry_record[a]["birth_date"]):
            decision.append("Accept")
        else:
            decision.append("Reject")

        # Check for valid Visa Date Format
        if entry_record[a]["entry_reason"] == "visit":
            if valid_date_format(entry_record[a]["visa"]["date"]):
                decision.append("Accept")
            else:
                decision.append("Reject")
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


"""
to get the keys of a dictionary, keys = dictionary.keys()
to check for empty strings, run a while loop checking for dictionary[keys[i]]
"""

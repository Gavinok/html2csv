#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# File:
#
# @author      : Gavin Jaeger-Freeborn (gavinfreeborn@gmail.com)
# @file        : table_to_csv.py
# @created     : Sat 30 Nov 2019 01:34:02 PM MST
# @description : This is a python3 program used to convert HTML tables to a CSV representation
#
# @Copyright © 2019 Gavin Jaeger-Freeborn gavinfreeborn@gmail.com
#
# Distributed under terms of the GPL license.

import os
import sys
import csv
import fileinput
import re

PLACEHOLDER = '++xxyyzz'

def containstable(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_tag('table', line)
    # tables = match_tag('table', line)

def endtable(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_end_tag('table', line)

def containsrow(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_tag('tr', line)

def endrow(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_end_tag('tr', line)

# only run when in table
def containshd(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_tag('th', line)

def endhd(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_end_tag('th', line)

# only run when in table
def containstd(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_tag('td', line)

def endtd(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_end_tag('td', line)

def match_end_tag(tag, line):
    """matches the end of a tag
    :returns: #  TODO: finish return <02-12-19 Gavin Jaeger-Freeborn>
    """
    regex = '</' + tag + '>'
    matchg = re.search(regex, line)
    if matchg:
        return 1
    return 0

def match_tag(tag, line):
    """matches the line against the given regex for a tag
    :returns: all matches if tag is found and 0 if not
    """
    regex = '<' + tag + '[^>]*>'

    line = re.sub('<' + tag + '[^>]*>', '<' + tag + '>', line)
    line = re.sub('</' + tag + '[^>]*>', '</' + tag + '>', line)
    lookregex = '(?<=<' + tag + '>)(.*?)?(?=</' + tag + '>)'
    # remove extra white space
    line = re.sub('\s+', ' ', line)
    matchg = re.search(regex, line)
    if matchg:
        matches = re.findall(lookregex, line)
        if matches:
            # for match in matches:
                # print("match for ", tag, " is ", match, "\n")
            return matches
    return 0

def clean_line(line):
    """ removes the non table related tags,
        puts a placeholder in empty tags,
        and removes newline character
    :returns: simplified line successful 0 if not
    """
    line = re.sub('></', '>' + PLACEHOLDER + '</', line)
    line = line.rstrip()
    return line

def remove_placeholders(row):
    """removes the placeholder each element in the given row
    :returns: the row without placeholders
    """
    corrected_row = []
    for item in row:
        if item == PLACEHOLDER:
            item = ''
        corrected_row.append(item)
    return corrected_row

def getheaders(rows):
    """gets the headers from the given rows as a list
    :returns: list of headers or 0 if none
    """
    fieldnames = []
    for row in rows:
        headers = containshd(row)
        if headers:
            headers_found = 1
            for header in headers:
                fieldnames.append(header)
    return fieldnames

def getdata(rows, headers):
    """gets the data from the given rows as a list of lists
    :returns: list for each row and a list data or 0 if none
    """
    tabledata = []
    for row in rows:
        data = containstd(row)
        # if data == 0:
            # print("error data is 0", "\n")
        if data:
            datalist = []
            for item in data:
                datalist.append(item)
            # print("datalist is", datalist, "\n")
            tabledata.append(datalist)
    return tabledata

def print_table(tableheaders, csvdata):
    """ print the given table to stdout
    :returns: 1 if successful 0 if not
    """
    writer = csv.writer(sys.stdout)

    # print table headers if they exist
    if len(tableheaders):
        writer.writerow(tableheaders)
        # append missing colombs
        # for i in csvdata:
        #     for j in i:

    # print the data for each row in the table
    for i in csvdata:
        for j in i:
            j = remove_placeholders(j)
            writer.writerow(j)
    return 1

def main():
    """ This is the main for my program"""

    states = { '0': 'not in table', '1': 'inside table', '2': 'inside row' }
    current_state = '0'
    # initialize command line argument options
    lines = ''
    try:
        for line in fileinput.input():
            # print(line, "\n")
            # print("new line ", "\n")
            # print(containstable(line),
            #       containsrow(line),
            #       containshd(line),
            #       endhd(line),
            #       containstd(line),
            #       endtd(line),
            #       endrow(line),
            #       endtable(line))
            lines += clean_line(line)
    except FileNotFoundError:
        print("Error: not html table to parse cannot be found or does not exist", file=sys.stderr)

    # print(lines)
    tables = containstable(lines)
    if tables:
        # print("tables is ", tables, "\n")
        headers_found = 0
        for table in tables:
            fieldnames = []
            csvdata = []
            # print("table is ", table, "\n")
            rows = containsrow(table)
            if not rows:
                print("error not rows", "\n")
            tableheaders = getheaders(rows)
            data = getdata(rows, fieldnames)
            csvdata.append(data)

            print_table(tableheaders, csvdata)
            print("\n")


if __name__ == '__main__':
    main()

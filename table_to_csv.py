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

    lookregex = '(?<=<' + tag + '>)(.*?)?(?=</' + tag + '>)'

    # remove extra data from tag
    line = re.sub('<' + tag + '[^>]*>', '<' + tag + '>', line)
    line = re.sub('</' + tag + '[^>]*>', '</' + tag + '>', line)
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
    line = re.sub('></', '>' + PLACEHOLDER + '</', line)
    line = line.rstrip()
    return line

def strip_element(row):
    """removes the placeholder each element in the given row
    :returns: the row without placeholders
    """
    #  TODO: use regex to remove just the PLACEHOLDER instead using exactly the placeholder <04-12-19 Gavin Jaeger-Freeborn>
    corrected_row = []
    for item in row:
        item = item.strip()
        item = item.replace(PLACEHOLDER, '')
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
        # print("data is ", data , "\n")
        if data:
            datalist = []
            for item in data:
                datalist.append(item)
            tabledata.append(datalist)

    return tabledata

def print_table(tableheaders, csvdata):
    """ print the given table to stdout
    :returns: 1 if successful 0 if not
    """
    # colnum = get_colnum(tableheaders, csvdata)
    # csvdata = append_cols(colnum, csvdata)
    # print("num of cols is ", colnum, "\n")

    writer = csv.writer(sys.stdout, lineterminator='\n')
    # print table headers if they exist
    if len(tableheaders):
        writer.writerow(tableheaders)

    # print the data for each row in the table
    for i in csvdata:
        for j in i:
            j = strip_element(j)
            writer.writerow(j)
    return 1

def append_cols(num, csvdata):
    """ensures all rows have the same number of columns as num
    :returns: csvdata with corrected number of column
    """
    for i in csvdata:
        for j in i:
            for x in range(num - len(j)):
                j.append('')
    return csvdata

def get_colnum(headers, csvdata):
    """ adds empty column to the rows that don't contain any data
    :returns: list of rows with corrected column number
    """
    colnum = -1
    if len(headers):
        colnum = len(headers)
        return colnum

    for table in csvdata:
        for row in table:
            cols = 0
            for i in row:
                cols += 1
            if cols > colnum:
                colnum = cols
    return colnum


def main():
    """ This is the main for my program"""
    if sys.stdin.isatty():
        sys.stderr.write("Error nothing set from stdin")
        sys.exit(1)

    # initialize command line argument options
    lines = ''
    try:
        for line in fileinput.input():
            # print(line, "\n")
            # print("new line ", "\n")
            line = clean_line(line)
            # print(containstable(line),
            #       containsrow(line),
            #       containshd(line),
            #       endhd(line),
            #       containstd(line),
            #       endtd(line),
            #       endrow(line),
            #       endtable(line))
            lines += line
    except FileNotFoundError:
        print("Error: not html table to parse cannot be found or does not exist", file=sys.stderr)

    # print(lines)
    tables = containstable(lines)
    if not tables:
        sys.stderr.write("Error no html table found in stdin")
        sys.exit(5)

    tablenumber = 1
    for table in tables:
        fieldnames = []
        csvdata = []
        rows = containsrow(table)

        # add data to empty rows to avoid ignoreing them
        for rowindex in range(len(rows)):
            if not containshd(rows[rowindex]) and not containstd(rows[rowindex]):
                # print("row is ", rows[rowindex], "\n")
                rows[rowindex] = '<td>' + PLACEHOLDER + '</td>'
                # print("no header or data in row", "\n")

        tableheaders = getheaders(rows)
        data = getdata(rows, fieldnames)
        csvdata.append(data)

        colnum = get_colnum(tableheaders, csvdata)
        csvdata = append_cols(colnum, csvdata)

        if tablenumber != 1:
            print()
        print("TABLE " + str(tablenumber) + ":")
        print_table(tableheaders, csvdata)
        # print("tables len i ", len(tables), "\n")
        tablenumber += 1
        # print("\n")


if __name__ == '__main__':
    main()

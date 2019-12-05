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

def containsrow(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_tag('tr', line)

# only run when in table
def containshd(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_tag('th', line)

# only run when in table
def containstd(line):
    """checks if the line contains a table declairation
    :returns: 0 if not table declairation returns 1 there is
    """
    return match_tag('td', line)

def match_end_tag(tag, line):
    """matches the end of a tag
    :returns: returns the number of closing tags for `tag`
    """
    regex = '</' + tag + '[^>]*>'
    matchg = re.findall(regex, line, re.IGNORECASE)
    if matchg:
        return len(matchg)
    return 0

def match_start_tag(tag, line):
    """matches the end of a tag
    :returns: the number of opening tag in line
    """
    regex = '<' + tag + '[^>]*>'
    matchg = re.findall(regex, line, re.IGNORECASE)
    if matchg:
        return len(matchg)
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

    matchg = re.search(regex, line, re.IGNORECASE)
    if matchg:
        matches = re.findall(lookregex, line, re.IGNORECASE)
        if matches:
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

def getdata(rows):
    """gets the data from the given rows as a list of lists
    :returns: list for each row and a list data or 0 if none
    """
    tabledata = []
    for row in rows:
        data = containstd(row)
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

def validate_line(line):
    """ check for invalid tags
    """
    # check for tags that have spaces before them
    if re.match('.*<(\s)+.*', line, re.IGNORECASE | re.DOTALL):
        sys.stderr.write("Error no spaces allowed between < and `tag`")
        sys.exit(3)

def validate_matching_tags(line):
    """takes the complete line and ensures that all tags have a matching closing tag
    """
    tags = ['tr', 'th', 'table', 'td']
    for tag in tags:
        if match_start_tag(tag, line) != match_end_tag(tag, line):
            sys.stderr.write("Error: unmatched tag", tag)
            sys.exit(4)

def main():
    """ This is the main for my program"""

    # check for standard input
    if sys.stdin.isatty():
        sys.stderr.write("Error nothing set from stdin")
        sys.exit(1)

    # initialize command line argument options
    lines = ''
    for line in fileinput.input():
        line = clean_line(line)
        validate_line(line)
        lines += line

    validate_matching_tags(lines)
    tables = containstable(lines)
    if not tables:
        sys.stderr.write("Error no html table found in stdin")
        sys.exit(5)

    tablenumber = 1
    for table in tables:
        csvdata = []
        rows = containsrow(table)

        # add data to empty rows to avoid ignoreing them
        for rowindex in range(len(rows)):
            if not containshd(rows[rowindex]) and not containstd(rows[rowindex]):
                rows[rowindex] = '<td>' + PLACEHOLDER + '</td>'

        tableheaders = getheaders(rows)
        data = getdata(rows)
        csvdata.append(data)

        # get the number of columns to put in every row
        colnum = get_colnum(tableheaders, csvdata)

        # apply the number of columns to each row
        csvdata = append_cols(colnum, csvdata)

        # print the appropriate spacing
        if tablenumber != 1:
            print()

        print("TABLE " + str(tablenumber) + ":")
        print_table(tableheaders, csvdata)
        tablenumber += 1


if __name__ == '__main__':
    main()

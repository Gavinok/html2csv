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

    line = re.sub('<' + tag + '[^>]*>','<' + tag + '>', line)
    line = re.sub('</' + tag + '[^>]*>','</' + tag + '>', line)
    lookregex = '(?<=<' + tag + '>)(.*?)?(?=</' + tag + '>)'
    # remove extra white space
    line = re.sub('\s+',' ', line)
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
    line = re.sub('></','>' + placeholder + '</',line)
    line = line.rstrip()
    return line

def clean_item(item):
    """removes the placeholder from the given element
    :returns: element without the placeholder
    """
    item = re.sub(placeholder, '', item)
    return item

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

def main():
    """ This is the main for my program"""

    states = { '0': 'not in table', '1': 'inside table', '2': 'inside row' }
    current_state = '0'
    # initialize command line argument options
    lines = ''
    try:
        for line in fileinput.input():
            # print(line, "\n")
            print("new line ", "\n")
            print(containstable(line),
                  containsrow(line),
                  containshd(line),
                  endhd(line),
                  containstd(line),
                  endtd(line),
                  endrow(line),
                  endtable(line))
            # print("line is before", line, "\n")
            # line = clean_tags(line)
            # print("line is after", line, "\n")
            lines += clean_line(line)
        print(lines)
        tables = containstable(lines)
        fieldnames = []
        if tables:
            # print("tables is ", tables, "\n")
            headers_found = 0
            for table in tables:
                csvdata = []
                print("table is ", table, "\n")
                rows = containsrow(table)
                if not rows:
                    print("error not rows", "\n")
                tableheaders = getheaders(rows)
                # csvdata.append(data)
               # if fieldnames:
               #     tableheaders[0]
                   # for tableheader in tableheaders:
                   #     #statements
                data = getdata(rows, fieldnames)
                csvdata.append(data)

                # for i in csvdata:
                #     print("table from csv is", i, "\n")
                writer = csv.writer(sys.stdout)
                for i in csvdata:
                    for j in i:
                        writer.writerow(j)
                print("\n")

        # print("csvdata is ", csvdata, "\n")

        #  TODO: switch from dictwrighter to wright by hand <02-12-19 Gavin Jaeger-Freeborn>
        # writer = csv.writer(sys.stdout)
        # for i in csvdata:
        #     writer.writerow(i)


        # with open(filename, mode='r', encoding='utf-8-sig') as csv_file:
        #     csv_reader = csv.DictReader(csv_file, delimiter=',')
        #     linenumber = 0
        #     for line in csv_reader:
        #         # make all enteries lowercase
        #         line = {k.lower(): v.lower() for k, v in line.items()}
        #         # test_args(filename, args,line,linenumber)
        #         data.append(line)
        #         linenumber += linenumber

    except FileNotFoundError:
        print("Error: ", filename, "cannot be found or does not exist", file=sys.stderr)

    # groups = []
    # if len(groups) > 20:
    #     print(" Error: ", filename, ":", args.group_by, "has been capped at 20 distinct values", args.group_by, "\n", file=sys.stderr)
    # # initialize csv and setup headers based on arguments
    # headers = getheaders(args)
    # complete_csv_dict = []

    # # if grouping the results
    # if args.group_by:

    #     # sort the data based on the groupings to be separated
    #     try:
    #         data = sorted(data, key=lambda k: k[args.group_by])
    #     except KeyError:
    #         print(" Error: ", filename, ":no group-by argument with name", args.group_by, "\n", file=sys.stderr)
    #         sys.exit(9)
    #     groups = seperate_groups(args.group_by, data)
    #     headers.insert(0, args.group_by)

    #     # separate into groups then determine the values for each row in the csv
    #     for i in groups:
    #         csventries = calc_val(filename, args, i)
    #         csventries[args.group_by] = i[0][args.group_by]
    #         complete_csv_dict.append(csventries)

    # else:
    #     # if not grouping the results
    #     csventries = calc_val(filename, args, data)
    #     complete_csv_dict.append(csventries)

    # writer = csv.DictWriter(sys.stdout, fieldnames=headers)
    # writer.writeheader()

    # for i in complete_csv_dict:
    #     writer.writerow(i)

if __name__ == '__main__':
    main()

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
import html
#  TODO: checkout using html.parser <01-12-19 Gavin Jaeger-Freeborn>

""" state mechine
table start     ts
table end       te
row start       rs
row end         re
Heading start   hs
Heading end     he
"""


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
            for match in matches:
                print("match for ", tag, " is ", match, "\n")
            return matches
    return 0

# def getheaders(rows):
#     """ finds the headers in the given rows
#     :returns: the headers as a list, 0 if no headers are found
#     """
#     #  TODO: finish getheaders <02-12-19 Gavin Jaeger-Freeborn>
#     for row in rows:
#         headers = containshd(row)
#         if headers:
#             headers_found = 1
#             for header in headers:
#                 fieldnames.append(header)

# def getdata(rows):
#     """ the data inside the given rows and converts it to a list of lists one list per row
#     :returns: Data as a list of list, 0 if no data is found
#     """
    #  TODO: finish getdata <02-12-19 Gavin Jaeger-Freeborn>

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
            print("line is before", line, "\n")
            line = re.sub('></','> </',line)
            print("line is after", line, "\n")
            lines += line.rstrip()
        print(lines)
        tables = containstable(lines)
        fieldnames = []
        csvdata = []
        if tables:
            # print("tables is ", tables, "\n")
            headers_found = 0
            for table in tables:
                print("table is ", table, "\n")
                rows = containsrow(table)
                if rows:
                    #headers = getheaders(rows)
                    #rows = getrows(rows)
                    for row in rows:
                        headers = containshd(row)
                        if headers:
                            headers_found = 1
                            for header in headers:
                                fieldnames.append(header)
                        data = containstd(row)
                        if data == 0:
                            print("error data is 0", "\n")
                        if data:
                            if headers_found:
                                datadict = {}
                                for index in range(len(fieldnames)):
                                    try:
                                        datadict[fieldnames[index]] = data[index]
                                    except IndexError:
                                        datadict[fieldnames[index]] = ''
                            # else:
                            #     datadict = []
                            # for item in data:
                            #     datadict.append(data[index])
                            csvdata.append(datadict)

        for i in csvdata:
            print("table from csv is", i, "\n")
        # print("csvdata is ", csvdata, "\n")

        #  TODO: switch from dictwrighter to wright by hand <02-12-19 Gavin Jaeger-Freeborn>

        # writer = csv.DictWriter(sys.stdout, fieldnames=headers)
        # writer.writeheader()

        # for i in complete_csv_dict:
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

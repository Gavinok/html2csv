######################################################################
# @author      : Gavin Jaeger-Freeborn (gavinfreeborn@gmail.com)
# @file        : Makefile
# @created     : Tue 19 Nov 2019 01:25:55 AM MST
######################################################################

CC=python3
FLAGS=-m codestyle
OBJ=./html2csv.py
TESTDIR=./tests
TESTSCRIPT=./test.sh

main: $(OBJ)
	$(CC) $(OBJ) $(FLAGS)

test:
	sh $(TESTSCRIPT)

clean:
	rm -f $(TESTDIR)/*/results.csv


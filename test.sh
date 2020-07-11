#!/bin/sh
./html2csv.py  <  tests/table_test_nomatch_tag/input.html    >  tests/table_test_nomatch_tag/results.csv
./html2csv.py  <  tests/table_test_badtag/input.html         >  tests/table_test_badtag/results.csv
./html2csv.py  <  tests/table_test_heavy/input.html          >  tests/table_test_heavy/results.csv
./html2csv.py  <  tests/table_test_heavy_oneline/input.html  >  tests/table_test_heavy_oneline/results.csv
./html2csv.py  <  tests/table_test_light/input.html          >  tests/table_test_light/results.csv
./html2csv.py  <  tests/table_test_medium/input.html         >  tests/table_test_medium/results.csv

diff  tests/table_test_nomatch_tag/output.txt    tests/table_test_nomatch_tag/results.csv
diff  tests/table_test_badtag/output.txt         tests/table_test_badtag/results.csv
diff  tests/table_test_heavy/output.txt          tests/table_test_heavy/results.csv
diff  tests/table_test_heavy_oneline/output.txt  tests/table_test_heavy_oneline/results.csv
diff  tests/table_test_light/output.txt          tests/table_test_light/results.csv
diff  tests/table_test_medium/output.txt         tests/table_test_medium/results.csv

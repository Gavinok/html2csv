#!/bin/sh
./table_to_csv.py < tests/table_test_heavy/input.html   > tests/table_test_heavy/results.csv
./table_to_csv.py < tests/table_test_heavy_oneline/input.html   > tests/table_test_heavy_oneline/results.csv
./table_to_csv.py < tests/table_test_light/input.html   > tests/table_test_light/results.csv
./table_to_csv.py < tests/table_test_medium/input.html  > tests/table_test_medium/results.csv

diff tests/table_test_heavy/output.txt    tests/table_test_heavy/results.csv
diff tests/table_test_heavy_oneline/output.txt    tests/table_test_heavy_oneline/results.csv
diff tests/table_test_light/output.txt    tests/table_test_light/results.csv
diff tests/table_test_medium/output.txt   tests/table_test_medium/results.csv

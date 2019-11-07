# AssociationAnalysis

The project has the implementation for Association rule mining using Apriori algorithm.

Use the file - Apriori.py for generating frequent item sets with the given minimum support

Sample usage:
````
python3 Apriori.py -database_file=database_small.txt -minsupp=0.1 -output_file=output.txt
````

The file Apriori.py takes 3 arguments:
1. database_file - it is the path to the database file which contains the list of all the transactions
2. minsupp - it is the threshold value based on which we get the frequent item sets
3. output_file - it is the path to store the frequent itemsets

Important note:
python3 should be used for the program to run successfully
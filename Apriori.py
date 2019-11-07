import argparse
import os
from collections import Counter
import itertools
import math


# method apriori to get the most frequent itemsets
# takes input - database file and minimum support
def apriori(database_file, min_support):
    # get the total number of transaction, number of items and list of transactions
    number_of_transactions, number_of_items, transaction_list = read_database(database_file)

    # calculating the support count based on the minimin support provided by the client
    _min_support_count = math.ceil(min_support * number_of_transactions)

    # getting the f1 set with most frequent 1-item set
    fk = generate_f1(transaction_list, _min_support_count)

    # final list where we will be storing all the frequent itemsets
    final_list = [fk]

    # total count of all the frequent itemsets
    final_count = len(fk)

    # actual_items has the f1 itemset, used for generating candidates
    actual_items = set(item for sublist in fk for item in sublist)
    k = 1
    while fk:
        # generate candidate itemsets
        lk_plus_1 = generate_candidate(fk, actual_items, k)

        # prune the candidates
        lk_plus_1 = prune_candidate(_lk_plus_1=lk_plus_1, _fk=fk, k=k)
        k += 1

        # get the support count for candidates
        support_dictionary = calculate_support(k, transaction_list, lk_plus_1)

        # eliminate the candidates based on the support count
        lk_plus_1 = eliminate_candidates(support_dictionary, lk_plus_1, _min_support_count)

        # if the lk_plus_1 is empty or None break from the loop
        if not lk_plus_1:
            break

        # update the fk to fk_plus_1 (lk_plus_1)
        fk = lk_plus_1
        final_count += len(fk)
        final_list.append(fk)

    return final_list, final_count, number_of_items


# function to eliminate candidates
# takes the following parameters:
#   support dictionary - which has the support counts for candidate sets
#   candidate list - list of candidates
#   min support count - threshold for minimum support count
def eliminate_candidates(_support_dictionary, _candidate_list, _min_support_count):
    # store the candidates whose min support count is greater than min_support count
    _final_list = set()
    for candidate in _candidate_list:
        # if the support count is greater than or equals to min support count add it to list
        if _support_dictionary.get(candidate, 0) >= _min_support_count:
            _final_list.add(candidate)
    return _final_list


# method to calculate support for each candidate list
def calculate_support(k, _transaction_list, _candidates_list):
    # a dictionary to store the frequency of the candidate list
    support_dictionary = dict()
    for candidate in _candidates_list:
        count = 0
        for transaction in _transaction_list:
            # if the candidate is a subset of the transaction then increase the count,
            # which is the support for the candidate
            if candidate.issubset(transaction):
                count += 1
        # once the counts are calculated add it to the dictionary
        support_dictionary[candidate] = count
    return support_dictionary


# this method is to prune the lk_plus_1 based on _fk
def prune_candidate(_lk_plus_1, _fk, k):
    # candidate list which contains pruned results
    _final_candidate_list = set()
    for _item_set in _lk_plus_1:
        # getting the combinations of size k for the item set
        # note that each item set in lk_plus_1 has size k+1
        combinations = itertools.combinations(_item_set, k)
        _is_present = True
        for x in combinations:
            # break the loop if a subset of the item set is not present in fk
            if frozenset(x) not in _fk:
                _is_present = False
                break
        # if present add it to the final candidate list
        if _is_present:
            _final_candidate_list.add(_item_set)

    return _final_candidate_list


# generate fk_plus_1 candidates based on the f1
def generate_candidate(item_set_list, actual_items, k):

    # stores the fk_plus_1 candidates
    _final_candidate_item_set_list = set()

    for item in actual_items:
        # if the item set is not in item set list then add it to the list
        for item_set in item_set_list:
            if item not in item_set:
                temp_set = set(item_set)
                temp_set.add(item)
                # adding it as frozen set because it can be hashed and searched easily
                temp_set = frozenset(temp_set)
                _final_candidate_item_set_list.add(temp_set)

    return _final_candidate_item_set_list


# get the f1 set from the list of transactions
def generate_f1(_transaction_list, _min_support):
    # using counter variable to get the counts of each item
    cnt = Counter(item for sublist in _transaction_list for item in sublist)
    # filter items based on the minimum support
    item_set = [frozenset([key]) for key, value in cnt.items() if value >= _min_support]
    return item_set


# Reading the data from the file
def read_database(_database_file_path):
    _data_file = open(_database_file_path, encoding="utf-8")
    _number_of_transactions = 0
    _number_of_items = 0
    # Getting the number of transactions and number of items
    for _line in _data_file:
        _split_lines = _line.split()
        _number_of_transactions = int(_split_lines[0])
        _number_of_items = int(_split_lines[1])
        break

    # Getting all the transactions present in the dataset
    _transaction_list = []
    for _line in _data_file:
        # storing them as frozensets
        _transaction_list.append(frozenset(_line.split()))

    _data_file.close()

    # returning number of transactions, number of items and transaction list
    return _number_of_transactions, _number_of_items, _transaction_list


# method to get the parser
def get_parser():
    _parser = argparse.ArgumentParser()

    # argument to get take the path of database file
    _parser.add_argument('-database_file')

    # argument to get take the minimum support
    _parser.add_argument('-minsupp')

    # argument to get take the path of output file
    _parser.add_argument('-output_file')

    return _parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    # get all the arguments required for the program to run
    database_file = os.path.abspath(str(args.database_file))
    min_support = float(str(args.minsupp))
    output_file = os.path.abspath(str(args.output_file))

    print(database_file)

    # get the final frequent item sets, total number of items and unique items
    final_result, final_count, number_of_items = apriori(database_file, min_support)

    answer = ''.join([str(final_count), " ", str(number_of_items), '\n'])

    # building a string for all the frequent itemsets
    for frequent in final_result:
        for item_set in frequent:
            y = ' '.join([str(elem) for elem in item_set])
            answer = ''.join([answer, y, '\n'])

    f = open(output_file, "w")

    # writing to the output file
    f.write(answer)

    f.close()


# main method where the program starts
if __name__ == '__main__':
    # see the main method for details
    main()

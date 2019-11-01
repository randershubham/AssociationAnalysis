import argparse
import os
from collections import Counter
import itertools
import math


def apriori(database_file, min_support):
    number_of_transactions, number_of_items, transaction_list = read_database(database_file)
    _min_support_count = math.ceil(min_support * number_of_transactions)

    fk = generate_f1(transaction_list, _min_support_count)
    actual_items = set(item for sublist in fk for item in sublist)
    k = 1
    while fk:
        lk_plus_1 = generate_candidate(fk, actual_items, k)
        lk_plus_1 = prune_candidate(_lk_plus_1=lk_plus_1, _fk=fk, k=k)
        k += 1
        support_dictionary = calculate_support(k, transaction_list, lk_plus_1)
        lk_plus_1 = eliminate_candidates(support_dictionary, lk_plus_1, _min_support_count)

        if not lk_plus_1:
            break
        fk = lk_plus_1

    return fk


def eliminate_candidates(_support_dictionary, _candidate_list, _min_support_count):
    _final_list = set()
    for candidate in _candidate_list:
        if _support_dictionary.get(candidate, 0) >= _min_support_count:
            _final_list.add(candidate)
    return _final_list


def calculate_support(k, _transaction_list, _candidates_list):
    support_dictionary = dict()
    for candidate in _candidates_list:
        count = 0
        for transaction in _transaction_list:
            if candidate.issubset(transaction):
                count += 1
        support_dictionary[candidate] = count
    return support_dictionary


def prune_candidate(_lk_plus_1, _fk, k):
    _final_candidate_list = set()
    for _item_set in _lk_plus_1:
        combinations = itertools.combinations(_item_set, k)
        _is_present = True
        for x in combinations:
            if frozenset(x) not in _fk:
                _is_present = False
                break
        if _is_present:
            _final_candidate_list.add(_item_set)

    return _final_candidate_list


def generate_candidate(item_set_list, actual_items, k):
    _final_candidate_item_set_list = set()

    # TODO: need to find efficient way to find candidates,
    # TODO: currently many redundant operations are being done
    # TODO: also do we need to create item set every time ?
    for item in actual_items:
        for item_set in item_set_list:
            if item not in item_set:
                temp_set = set(item_set)
                temp_set.add(item)
                temp_set = frozenset(temp_set)
                _final_candidate_item_set_list.add(temp_set)

    return _final_candidate_item_set_list


def generate_f1(_transaction_list, _min_support):
    cnt = Counter(item for sublist in _transaction_list for item in sublist)
    # TODO: do we need frozenset?
    item_set = [frozenset([key]) for key, value in cnt.items() if value >= _min_support]
    return item_set


def read_database(_database_file_path):
    _data_file = open(_database_file_path, encoding="utf-8")
    _number_of_transactions = 0
    _number_of_items = 0
    for _line in _data_file:
        _split_lines = _line.split()
        _number_of_transactions = int(_split_lines[0])
        _number_of_items = int(_split_lines[1])
        break

    _transaction_list = []
    for _line in _data_file:
        _transaction_list.append(frozenset(_line.split()))

    _data_file.close()
    return _number_of_transactions, _number_of_items, _transaction_list


def get_parser():
    _parser = argparse.ArgumentParser()

    _parser.add_argument('-database_file')
    _parser.add_argument('-minsupp')
    _parser.add_argument('-output_file')

    return _parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    # get all the arguments required for the program to run
    database_file = os.path.abspath(str(args.database_file))
    min_support = float(str(args.minsupp))
    output_file = os.path.abspath(str(args.output_file))

    final_result = apriori(database_file, min_support)

    f = open(output_file, "w")

    for item_set in final_result:
        f.writelines(' '.join([str(elem) for elem in item_set]))
        f.write('\n')

    f.close()


# main method where the program starts
if __name__ == '__main__':
    main()

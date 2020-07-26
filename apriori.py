import sys
from collections import defaultdict
from collections import Iterable

freq_itemsets = defaultdict(lambda: defaultdict(int))

def load_data(file):
    data = []
    for line in file.readlines():
        data.append(line.strip().split(';'))
    file.close()
    return data

def check_freq(itemset, data, min_sup):
    freq = 0
    for record in data:
        if itemset.issubset(set(record)):
            freq += 1
    return freq > min_sup, freq

def get_freq_itemsets_size_one(data, min_sup):
    freq = defaultdict(int)
    for record in data:
        for item in record:
            freq[item] += 1
    return {frozenset([item]): freq[item] for item in freq if freq[item] > min_sup}

def get_items(itemsets):
    items = set()
    for itemset in itemsets:
        for item in itemset:
            items.add(item)
    return items

def get_next_level_candidates(itemsets):
    """Generate candidate frequent itemsets of size k+1, from that of size k.

    Args:
        patterns (Iterable of sets of size k): Frequent itemsets of size k.

    Returns:
        set of frozensets of size k+1: Candidate frequent itemsets of size k+1.
    """
    items = get_items(itemsets)
    raw_candidates = set()
    candidates = set()
    for itemset in itemsets:
        for item in items:
            if item not in itemset:
                new_itemset = itemset.union(set([item]))
                raw_candidates.add(frozenset(new_itemset))
    for itemset in raw_candidates:
        for item in itemset:
            sub_itemset = itemset - set([item])
            if not sub_itemset.issubset(itemsets):
                break
        candidates.add(itemset)
    return candidates

def get_next_level_itemsets(level, data, min_sup):
    if level == 1:
        freq_itemsets[1] = get_freq_itemsets_size_one(data, min_sup)
    elif level > 1:
        current_patterns = freq_itemsets[level - 1]
        candidates = get_next_level_candidates(current_patterns)
        for itemset in candidates:
            is_freq, freq = check_freq(pattern, data, min_sup)
            if is_freq:
                freq_itemsets[level][itemset] = freq

def apriori(data, min_sup):
    finished = False
    level = 1
    while not finished:
        print(level)
        get_next_level_itemsets(level, data, min_sup)
        if level not in freq_itemsets:
            finished = True
        level += 1

def save_freq_itemsets(output_file_name):
    with open('freq_itemsets_' + output_file_name, 'w') as f:
        for level in freq_itemsets:
            for itemset in freq_itemsets[level]:
                f.write("{}:{}\n".format(freq_itemsets[level][itemset], ';'.join(itemset)))
    with open('single_freq_items_' + output_file_name, 'w') as f:
        for itemset in freq_itemsets[1]:
            f.write("{}:{}\n".format(freq_itemsets[1][itemset], min(itemset)))            

def main():
    file = open(sys.argv[1])
    min_sup = int(sys.argv[2])
    data = load_data(file)
    apriori(data, min_sup)
    output_file_name = "min_support_{}.txt".format(min_sup)
    save_freq_itemsets(output_file_name)

if __name__ == '__main__':
    main()

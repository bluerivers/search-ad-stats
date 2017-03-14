import itertools


def generate_keyword_permutations(keyword_collection):
    delimiter = ' '

    if len(keyword_collection) < 1:
        return []
    elif len(keyword_collection) == 1:
        return keyword_collection[0]

    ret = []
    for selected_number in range(2, len(keyword_collection) + 1):
        for selected_list in itertools.permutations(keyword_collection, selected_number):
            for result in itertools.product(*selected_list):
                for element in itertools.permutations(result):
                    ret.append(delimiter.join(element))
    return ret



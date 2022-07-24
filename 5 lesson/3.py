#3


def make_super_list(langs, indices):
    return [(index, lang.upper()) for index, lang in zip(indices, langs)]


def get_devisors(num):
    devisors = []
    for devisor in range(1, num + 1):
        if num % devisor == 0:
            devisors.append(devisor)
    return devisors

def filer_super_list(super_list):
    filtered_list = []
    for old_index, lang in super_list:
        new_index = sum(ord(s) for s in lang)
        devisors = get_devisors(new_index)
        # this print is for debugging purpose:
        # print(f'Checking if {old_index} in ({new_index}) -> {devisors}')
        if old_index in devisors:
            filtered_list.append((new_index, lang))
    return filtered_list


if __name__ == "__main__":
    programming_languages = [
        'python',
        'java',
        'C++',
        'Assembly',
        'Haskel',
        'C#',
        'C',
        'TypeScript',
        'JavaScript',
        'R',
        'Bash',
    ]

    print(f'Original list: {programming_languages}')
    indices = [i for i in range(1, len(programming_languages) + 1)]
    super_list = make_super_list(programming_languages, indices)
    print(f'Modified list: {super_list}')
    new_list = filer_super_list(super_list)
    print(f'Filtered list: {new_list}')
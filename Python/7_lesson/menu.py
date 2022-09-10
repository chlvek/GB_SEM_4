from interactive_input import input_digit


def choose(title: str, options: dict):
    pretty_title = f'{"="*20} {title} {"="*20}'
    bottom_line = '=' * (20 + 20 + len(title) + 2)

    print(pretty_title)
    for num, option_name in enumerate(options, start=1):
        print(f'{num}: {option_name}')
    option = input_digit('Input: ', 1, len(options))
    print(bottom_line)

    return option - 1



def run_menu(title: str, options: dict):
    '''Run a menu with the given title and options.'''
    while True:
        option = choose(title, options.keys())
        list(options.items())[option][1]()
        
        
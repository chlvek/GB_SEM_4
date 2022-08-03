'''
Menu:
    1 - Show records
    2 - Search
        2.1 - by name
        2.2 - by lastname
    3 - Add person (suggest export?)
    4 - Delete person (search -> delete)
    6 - Import/Export
        6.1 Import from file
        6.2 Export to file
            6.2.1 Chose format (csv, json, txt)
            6.2.2 Create new file
'''

import phonebook
from interactive_input import input_phone, yn_dialog
from menu import choose, run_menu


def show_records():
    records = phonebook.get_records()
    if not records:
        print('No records to show')
        return
    for i, record in enumerate(records, start=1):
        print(f'{i}: {record}')


def search_record() -> None:
    search_options = {
        'By name': phonebook.search_by_name,
        'By lastname': phonebook.search_by_lastname,
    }
    by = choose('SEARCH', search_options.keys())
    search_data = input('What to search: ')
    found = list(search_options.items())[by][1](search_data)
    if found:
        print(f'Found person: {phonebook.pretty_record(found)}')
    else:
        print(f'No person found')


def add_record():
    lastname = input('Input lastname: ')
    name = input('Input name: ')
    phone = input_phone()
    info = input('Input info: ')
    phonebook.add(lastname, name, phone, info)


def delete_record():
    record_index = choose('DELETE', phonebook.get_records())
    record = phonebook.get_record(record_index)
    phonebook.delete(record_index)
    print(f'Deleted: {phonebook.pretty_record(record)}')


def import_export():
    io = choose('IMPORT/EXPORT', ['Import', 'Export', 'Back'])
    if io == 0:  # import
        if not phonebook.FILES_DATA:
            print('No data to import')
            return
        if phonebook.UNSAVED_CHANGES:
            sure = yn_dialog('You have unsaved changes. Are you sure you want to continue?: ')
            if not sure:
                print('Import stopped')
                return
        f = list(phonebook.FILES_DATA)[choose('IMPORT FILE', phonebook.FILES_DATA)]
        phonebook.import_data(f)
    if io == 1:  # export
        filename = input('File name: ')
        fmt = phonebook.FORMATS[choose('FILE FORMAT', phonebook.FORMATS)]
        if '.'.join((filename, fmt)) in phonebook.FILES_DATA:
            print('This file is already exists')
            return
        phonebook.export_data(filename, fmt)


def exit_app():
    sure = yn_dialog('You have unsaved changes. Are you sure you want to exit?: ') if phonebook.UNSAVED_CHANGES else True
    if sure:
        print('Bye!')
        exit()


def main():
    phonebook.load_files_data()
    main_menu_options = {
        'Show records': show_records,
        'Search': search_record,
        'Add': add_record,
        'Delete': delete_record,
        'Import/Export': import_export,
        'Exit': exit_app,
    }
    run_menu('PHONEBOOK', main_menu_options)


if __name__ == "__main__":
    main()
    
    
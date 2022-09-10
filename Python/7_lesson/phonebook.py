from os import listdir
from os.path import join, dirname
from re import U
from import_export import (
    import_csv,
    import_json,
    import_txt,
    export_csv,
    export_json,
    export_txt,
)


IMPORTERS = {
    'csv': import_csv,
    'json': import_json,
    'txt': import_txt,
}
EXPORTERS = {
    'csv': export_csv,
    'json': export_json,
    'txt': export_txt,
}
FORMATS = ('csv', 'json', 'txt')
UNSAVED_CHANGES = False
DATA_DIR = None
FILES_DATA = {}
PEOPLE_DATA = {}


def load_files_data():
    '''Get data about imported/exported files.'''
    global FILES_DATA, DATA_DIR
    DATA_DIR = join(dirname(__file__), '.data')
    files = listdir(DATA_DIR)
    files_data = {}
    for file_name in files:
        info = file_name.split('.')
        if info[-1] in FORMATS:
            files_data[file_name] = join(DATA_DIR, file_name)
    FILES_DATA = files_data


def pretty_record(record):
    (lastname, name), data = record
    phone, info = data['phone'], data['info']
    return f'{lastname.title()} {name.title()}: {phone} ({info})'


def get_record(index):
    return list(PEOPLE_DATA.items())[index]


def get_records():
    global PEOPLE_DATA
    return [pretty_record(r) for r in PEOPLE_DATA.items()]


def search_by_lastname(desired_last_name):
    global PEOPLE_DATA
    for person, info in PEOPLE_DATA.items():
        lastname, name = person
        if lastname.lower() == desired_last_name.lower():
            return person, info
    return None


def search_by_name(desired_name):
    global PEOPLE_DATA
    for person, info in PEOPLE_DATA.items():
        lastname, name = person
        if name.lower() == desired_name.lower():
            return person, info
    return None


def find(key):
    global PEOPLE_DATA
    return PEOPLE_DATA.get(key)


def add(lastname, name, phone, info):
    global PEOPLE_DATA, UNSAVED_CHANGES
    PEOPLE_DATA[(lastname, name)] = {'phone': phone, 'info': info}
    UNSAVED_CHANGES = True


def delete(index):
    global PEOPLE_DATA
    key = list(PEOPLE_DATA)[index]
    del PEOPLE_DATA[key]
    UNSAVED_CHANGES = True


def import_data(filename):
    global PEOPLE_DATA, FILES_DATA, UNSAVED_CHANGES
    path = FILES_DATA[filename]
    fmt = filename.split('.')[-1]
    importer = IMPORTERS[fmt]
    data = importer(path)
    PEOPLE_DATA = data
    UNSAVED_CHANGES = False
    # print(f'import from: {path}')


def add_file(filename, fmt):
    f = '.'.join((filename, fmt))
    new_path = join(DATA_DIR, f)
    FILES_DATA[f] = new_path
    return new_path


def export_data(filename, fmt):
    global PEOPLE_DATA, UNSAVED_CHANGES
    path = add_file(filename, fmt)
    exporter = EXPORTERS[fmt]
    exporter(PEOPLE_DATA, path)
    UNSAVED_CHANGES = False
    
    